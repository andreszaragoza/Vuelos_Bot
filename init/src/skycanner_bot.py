import requests
import json
import time
import threading
from datetime import datetime, timedelta
from typing import List, Dict, Optional

class SkyscannerBot:
    """Bot para buscar vuelos baratos usando la API de Skyscanner"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://partners.api.skyscanner.net/apiservices/v3/flights/live"
        self.headers = {
            'x-api-key': api_key,
            'Content-Type': 'application/json'
        }
        self.alertas = []
        self.ejecutando = False
    
    def crear_busqueda(self, origen: str, destino: str, fecha_ida: datetime, 
                      fecha_vuelta: Optional[datetime] = None, adultos: int = 1) -> Optional[Dict]:
        """Crear una nueva búsqueda de vuelos"""
        
        query = {
            "market": "ES",
            "locale": "es-ES",
            "currency": "EUR",
            "queryLegs": [
                {
                    "originPlaceId": {"iata": origen},
                    "destinationPlaceId": {"iata": destino},
                    "date": {"year": fecha_ida.year, "month": fecha_ida.month, "day": fecha_ida.day}
                }
            ],
            "adults": adultos,
            "cabinClass": "CABIN_CLASS_ECONOMY"
        }
        
        if fecha_vuelta:
            query["queryLegs"].append({
                "originPlaceId": {"iata": destino},
                "destinationPlaceId": {"iata": origen},
                "date": {"year": fecha_vuelta.year, "month": fecha_vuelta.month, "day": fecha_vuelta.day}
            })
        
        try:
            response = requests.post(
                f"{self.base_url}/search/create",
                headers=self.headers,
                json=query,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error creando búsqueda: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error en la petición: {e}")
            return None
    
    def obtener_resultados(self, session_token: str) -> Optional[Dict]:
        """Obtener resultados de una búsqueda"""
        
        try:
            response = requests.post(
                f"{self.base_url}/search/poll",
                headers=self.headers,
                json={"sessionToken": session_token},
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error obteniendo resultados: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error en la petición: {e}")
            return None
    
    def buscar_vuelos_baratos(self, origen: str, destino: str, fecha_ida: datetime, 
                             fecha_vuelta: Optional[datetime] = None, 
                             precio_max: Optional[float] = None) -> List[Dict]:
        """Buscar vuelos y filtrar por precio"""
        
        print(f"🔍 Buscando vuelos {origen} → {destino}...")
        
        busqueda = self.crear_busqueda(origen, destino, fecha_ida, fecha_vuelta)
        if not busqueda:
            return []
        
        session_token = busqueda.get('sessionToken')
        if not session_token:
            return []
        
        time.sleep(5)
        
        resultados = self.obtener_resultados(session_token)
        if not resultados:
            return []
        
        # Procesar resultados
        vuelos_baratos = []
        content = resultados.get('content', {})
        results = content.get('results', {})
        itinerarios = results.get('itineraries', {})
        
        for itinerario_id, itinerario in itinerarios.items():
            pricing_options = itinerario.get('pricingOptions', [])
            if not pricing_options:
                continue
                
            precio = pricing_options[0].get('price', {}).get('amount', 0)
            
            if precio_max is None or precio <= precio_max:
                vuelo = {
                    'id': itinerario_id,
                    'precio': precio,
                    'origen': origen,
                    'destino': destino,
                    'fecha_ida': fecha_ida.strftime('%Y-%m-%d'),
                    'fecha_vuelta': fecha_vuelta.strftime('%Y-%m-%d') if fecha_vuelta else None,
                    'detalles': itinerario
                }
                vuelos_baratos.append(vuelo)
        
        vuelos_baratos.sort(key=lambda x: x['precio'])
        return vuelos_baratos[:5]
    
    def agregar_alerta(self, origen: str, destino: str, precio_max: float, 
                      fecha_ida: datetime, fecha_vuelta: Optional[datetime] = None):
        """Agregar una alerta de precio"""
        alerta = {
            'origen': origen,
            'destino': destino,
            'precio_max': precio_max,
            'fecha_ida': fecha_ida,
            'fecha_vuelta': fecha_vuelta,
            'activa': True,
            'mejor_precio_encontrado': float('inf'),
            'creada': datetime.now()
        }
        self.alertas.append(alerta)
        print(f"✅ Alerta creada: {origen} → {destino} por menos de {precio_max}€")
    
    def verificar_alertas(self):
        """Verificar todas las alertas activas"""
        print(f"🔍 Verificando {len(self.alertas)} alertas... ({datetime.now().strftime('%H:%M:%S')})")
        
        for i, alerta in enumerate(self.alertas):
            if not alerta['activa']:
                continue
            
            print(f"   Verificando alerta {i+1}/{len(self.alertas)}: {alerta['origen']} → {alerta['destino']}")
            
            vuelos = self.buscar_vuelos_baratos(
                alerta['origen'],
                alerta['destino'],
                alerta['fecha_ida'],
                alerta['fecha_vuelta'],
                alerta['precio_max']
            )
            
            if vuelos:
                mejor_precio = vuelos[0]['precio']
                if mejor_precio < alerta['mejor_precio_encontrado']:
                    alerta['mejor_precio_encontrado'] = mejor_precio
                    self.notificar_oferta(vuelos[0])
                    print(f"   ✅ Nuevo mejor precio: {mejor_precio}€")
                else:
                    print(f"   📊 Precio actual: {mejor_precio}€")
            else:
                print(f"   ❌ No se encontraron vuelos")
            
            time.sleep(2)
    
    def notificar_oferta(self, vuelo: Dict):
        """Notificar cuando se encuentra una oferta"""
        mensaje = f"""
🎉 ¡OFERTA ENCONTRADA! 🎉
✈️ {vuelo['origen']} → {vuelo['destino']}
💰 Precio: {vuelo['precio']}€
📅 Fecha ida: {vuelo['fecha_ida']}
📅 Fecha vuelta: {vuelo['fecha_vuelta'] or 'Solo ida'}
⏰ Encontrado: {datetime.now().strftime('%d/%m/%Y %H:%M')}
        """
        print(mensaje)
        print("-" * 50)
    
    def guardar_alertas(self, archivo: str = "data/alertas.json"):
        """Guardar alertas en archivo JSON"""
        alertas_serializables = []
        for alerta in self.alertas:
            alerta_copia = alerta.copy()
            # Convertir datetime a string para JSON
            alerta_copia['fecha_ida'] = alerta['fecha_ida'].isoformat()
            if alerta['fecha_vuelta']:
                alerta_copia['fecha_vuelta'] = alerta['fecha_vuelta'].isoformat()
            alerta_copia['creada'] = alerta['creada'].isoformat()
            alertas_serializables.append(alerta_copia)
        
        with open(archivo, 'w') as f:
            json.dump(alertas_serializables, f, indent=2)
        print(f"✅ Alertas guardadas en {archivo}")
    
    def cargar_alertas(self, archivo: str = "data/alertas.json"):
        """Cargar alertas desde archivo JSON"""
        try:
            with open(archivo, 'r') as f:
                alertas_data = json.load(f)
            
            self.alertas = []
            for alerta_data in alertas_data:
                alerta = alerta_data.copy()
                # Convertir strings de vuelta a datetime
                alerta['fecha_ida'] = datetime.fromisoformat(alerta_data['fecha_ida'])
                if alerta_data['fecha_vuelta']:
                    alerta['fecha_vuelta'] = datetime.fromisoformat(alerta_data['fecha_vuelta'])
                alerta['creada'] = datetime.fromisoformat(alerta_data['creada'])
                self.alertas.append(alerta)
            
            print(f"✅ {len(self.alertas)} alertas cargadas desde {archivo}")
        except FileNotFoundError:
            print(f"⚠️ Archivo {archivo} no encontrado. Empezando con alertas vacías.")
        except Exception as e:
            print(f"❌ Error cargando alertas: {e}")