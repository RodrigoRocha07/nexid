from sqlalchemy.exc import OperationalError, DisconnectionError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import logging
import time
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



# Criar o engine do SQLA#lchemy
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=20,        # Tamanho do pool de conexões
    max_overflow=20,     # Número máximo de conexões adicionais
    pool_recycle=3600,   # Reciclar conexões após 1 hora
    pool_timeout=30      # Tempo máximo de espera para uma conexão do pool (30 segundos)
)

# Configurar SessionLocal para criar sessões de banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa para mapeamento das tabelas
Base = declarative_base()

def criar_db():
    """Cria as tabelas no banco de dados se não existirem."""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Gerenciador de sessão do banco de dados com tentativas de reconexão."""
    retries = 3  # Número de tentativas de reconexão
    for attempt in range(retries):
        db = None
        try:
            db = SessionLocal()
            logger.info(f"Tentativa {attempt + 1}: Conexão ao banco de dados estabelecida.")
            yield db
            break  # Conexão bem-sucedida, sair do loop
        except (OperationalError, DisconnectionError) as e:
            logger.warning(f"Tentativa {attempt + 1} falhou com erro: {e}")
            if attempt < retries - 1:
                time.sleep(5)  # Esperar antes de tentar novamente
            else:
                logger.error("Todas as tentativas de conexão falharam. Levantando exceção.")
                raise e  # Levantar exceção se todas as tentativas falharem
        finally:
            if db:
                db.close()
                logger.info("Conexão ao banco de dados fechada.")
