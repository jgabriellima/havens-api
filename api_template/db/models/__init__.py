from api_template.db.models.assistant import Assistant, setup_relationships as setup_assistant_relationships
from api_template.db.models.client import Client, setup_relationships as setup_client_relationships
from api_template.db.models.session import Session, setup_relationships as setup_session_relationships
from api_template.db.models.client_user import ClientUser, setup_relationships as setup_client_user_relationships
from api_template.db.models.client_end_user import ClientEndUser, setup_relationships as setup_client_end_user_relationships
from api_template.db.models.communication_channel import CommunicationChannel, setup_relationships as setup_channel_relationships
from api_template.db.models.message import Message, setup_relationships as setup_message_relationships
from api_template.db.models.event import Event, setup_relationships as setup_event_relationships
from api_template.db.models.call import Call, setup_relationships as setup_call_relationships

# Configurar relacionamentos na ordem correta
setup_event_relationships()
setup_message_relationships()
setup_call_relationships()
setup_client_user_relationships()
setup_client_end_user_relationships()
setup_channel_relationships()
setup_session_relationships()
setup_assistant_relationships()
setup_client_relationships()
