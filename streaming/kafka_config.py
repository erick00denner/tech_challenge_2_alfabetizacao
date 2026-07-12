"""
Configurações do módulo de Streaming.

Este módulo centraliza todas as configurações utilizadas
pelo Producer e Consumer Kafka.
"""

# ============================================================================
# Kafka
# ============================================================================

BOOTSTRAP_SERVERS = "localhost:9092"

TOPIC = "alfabetizacao-indicadores"

GROUP_ID = "gold-consumer"

AUTO_OFFSET_RESET = "earliest"

ENABLE_AUTO_COMMIT = True

# ============================================================================
# Simulação
# ============================================================================

EVENTS_PER_EXECUTION = 10

RANDOM_SEED = 42