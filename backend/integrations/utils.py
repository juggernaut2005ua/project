import requests
import json
from .models import IntegrationTask, DataMapping

def sync_data_between_systems(task):
    """Синхронизирует данные между двумя системами"""
    records_synced = 0
    
    try:
        # Получаем данные из первой системы
        data_a = fetch_data_from_system(task.system_a)
        
        # Применяем маппинги
        mappings = task.mappings.all()
        transformed_data = transform_data(data_a, mappings)
        
        # Отправляем во вторую систему
        records_synced = send_data_to_system(task.system_b, transformed_data)
        
        return {'records_synced': records_synced, 'status': 'success'}
    
    except Exception as e:
        raise Exception(f'Ошибка при синхронизации: {str(e)}')

def fetch_data_from_system(system):
    """Получает данные из системы"""
    headers = {'Authorization': f'Bearer {system.api_key}'}
    try:
        response = requests.get(f'{system.api_endpoint}/data', headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise Exception(f'Ошибка при получении данных: {str(e)}')

def send_data_to_system(system, data):
    """Отправляет данные в систему"""
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
        raise Exception(f'Ошибка при отправке данных: {str(e)}')

def transform_data(data, mappings):
    """Трансформирует данные согласно маппингам"""
    if isinstance(data, list):
        return [transform_single_record(record, mappings) for record in data]
    else:
        return transform_single_record(data, mappings)

def transform_single_record(record, mappings):
    """Трансформирует отдельную запись"""
    transformed = {}
    for mapping in mappings:
        if mapping.field_a in record:
            value = record[mapping.field_a]
            if mapping.transformation_rule:
                try:
                    rule = json.loads(mapping.transformation_rule)
                    value = apply_transformation(value, rule)
                except:
                    pass
            transformed[mapping.field_b] = value
    return transformed

def apply_transformation(value, rule):
    """Применяет правило трансформации"""
    if rule.get('type') == 'uppercase':
        return str(value).upper()
    elif rule.get('type') == 'lowercase':
        return str(value).lower()
    elif rule.get('type') == 'multiply':
        return value * rule.get('factor', 1)
    return value
