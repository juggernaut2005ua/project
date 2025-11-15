# backend/integrations/utils.py - ROZSZERZONE
import requests
import json
from .models import IntegrationTask, DataMapping
import logging

logger = logging.getLogger(__name__)

def test_system_connection(system):
    """Testuje połączenie z systemem"""
    headers = {'Authorization': f'Bearer {system.api_key}'}
    try:
        response = requests.get(
            f'{system.api_endpoint}/health',
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        return {
            'status_code': response.status_code,
            'response_time': response.elapsed.total_seconds()
        }
    except requests.RequestException as e:
        raise Exception(f'Błąd połączenia: {str(e)}')


def sync_data_between_systems(task):
    """Synchronizuje dane między systemami"""
    records_synced = 0
    errors = []
    
    try:
        logger.info(f"Rozpoczynam synchronizację dla zadania: {task.name}")
        
        # Pobierz dane ze źródła
        if task.direction in ['a_to_b', 'bidirectional']:
            data_a = fetch_data_from_system(task.system_a)
            mappings = task.mappings.all()
            transformed_data = transform_data(data_a, mappings)
            records_synced += send_data_to_system(task.system_b, transformed_data)
        
        if task.direction in ['b_to_a', 'bidirectional']:
            data_b = fetch_data_from_system(task.system_b)
            mappings = task.mappings.all()
            transformed_data = transform_data(data_b, mappings)
            records_synced += send_data_to_system(task.system_a, transformed_data)
        
        logger.info(f"Synchronizacja zakończona. Zsynchronizowano {records_synced} rekordów")
        
        return {
            'records_synced': records_synced,
            'status': 'success',
            'errors': errors
        }
    
    except Exception as e:
        logger.error(f"Błąd podczas synchronizacji: {str(e)}")
        raise


def fetch_data_from_system(system):
    """Pobiera dane z systemu"""
    headers = {'Authorization': f'Bearer {system.api_key}'}
    try:
        response = requests.get(
            f'{system.api_endpoint}/data',
            headers=headers,
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise Exception(f'Błąd przy pobieraniu danych z {system.name}: {str(e)}')


def send_data_to_system(system, data):
    """Wysyła dane do systemu"""
    headers = {
        'Authorization': f'Bearer {system.api_key}',
        'Content-Type': 'application/json'
    }
    try:
        response = requests.post(
            f'{system.api_endpoint}/data',
            json=data,
            headers=headers,
            timeout=30
        )
        response.raise_for_status()
        return len(data) if isinstance(data, list) else 1
    except requests.RequestException as e:
        raise Exception(f'Błąd przy wysyłaniu danych do {system.name}: {str(e)}')


def transform_data(data, mappings):
    """Transformuje dane zgodnie z mapowaniem"""
    if isinstance(data, list):
        return [transform_single_record(record, mappings) for record in data]
    else:
        return transform_single_record(data, mappings)


def transform_single_record(record, mappings):
    """Transformuje pojedynczy rekord"""
    transformed = {}
    
    for mapping in mappings:
        if mapping.field_a in record:
            value = record[mapping.field_a]
            
            # Zastosuj reguły transformacji
            if mapping.transformation_rule:
                try:
                    rule = json.loads(mapping.transformation_rule)
                    value = apply_transformation(value, rule)
                except json.JSONDecodeError:
                    logger.warning(f"Nieprawidłowa reguła transformacji dla {mapping.field_a}")
            
            transformed[mapping.field_b] = value
        elif mapping.is_required:
            raise ValueError(f"Brak wymaganego pola: {mapping.field_a}")
    
    return transformed


def apply_transformation(value, rule):
    """Aplikuje regułę transformacji"""
    rule_type = rule.get('type')
    
    if rule_type == 'uppercase':
        return str(value).upper()
    elif rule_type == 'lowercase':
        return str(value).lower()
    elif rule_type == 'multiply':
        return value * rule.get('factor', 1)
    elif rule_type == 'add':
        return value + rule.get('amount', 0)
    elif rule_type == 'format_date':
        from datetime import datetime
        try:
            dt = datetime.fromisoformat(value)
            return dt.strftime(rule.get('format', '%Y-%m-%d'))
        except:
            return value
    
    return value
