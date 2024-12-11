# Sistema de Gestão Multi-Cliente e Comunicação Multi-Camada

## 1. Overview do Sistema

O sistema é o núcleo de uma solução que permite comunicação, interação e gestão de empresas (clientes), seus usuários internos (e.g., corretores, administradores) e usuários-clientes (e.g., compradores, investidores), suportando diversos canais de comunicação e funcionalidades personalizadas para assistentes inteligentes.

### Principais Funcionalidades
#### Gestão de Clientes:

- Cadastro, configuração e associação de canais.
- Integração de planos de subscrição com serviços externos (e.g., Stripe).

#### Gestão de Usuários Internos e Usuários-Clientes:

- Registro de usuários internos (e.g., corretores).
- Registro de usuários-clientes vinculados a usuários internos (e.g., compradores).

### Gestão de Assistentes:

- Associação de assistentes inteligentes a clientes.
- Configuração de ferramentas específicas para os assistentes.

### Comunicação Multi-Modal:

- Suporte a mensagens via WhatsApp.
- Suporte a chamadas de voz (Inbound e Outbound).
- Registro detalhado de mensagens, chamadas e eventos.

### Processamento Assíncrono:

- Execução de tarefas em segundo plano, como transcrição de áudios e consultas a APIs externas.

### Observabilidade Total:

- Registro de eventos operacionais para rastreamento completo e diagnóstico.

## 2. Modelo de Dados Atualizado

Entidades Principais

### Clientes (Clients)
- ClientID: Identificador único.
- ClientName: Nome do cliente.
- AdditionalInfo: Informações adicionais.
- CreatedAt: Data de criação.
- UpdatedAt: Data de atualização.

### Usuários Internos (ClientUsers)
- UserID: Identificador único.
- ClientID: Referência ao cliente.
- UserName: Nome do usuário.
- UserRole: Função básica (e.g., 'Administrador', 'Corretor').
- Email: E-mail.
- PhoneNumber: Número de telefone.
- ExternalUserID: Identificador em sistema externo.
- Status: Status do usuário.
- CreatedAt: Data de criação.
- UpdatedAt: Data de atualização.

### Usuários-Clientes (ClientEndUsers)
- EndUserID: Identificador único.
- ClientID: Referência ao cliente.
- UserID: Referência ao corretor responsável.
- Name: Nome do usuário-cliente.
- Email: E-mail.
- PhoneNumber: Número de telefone.
- AdditionalInfo: Informações adicionais (e.g., preferências).
- Status: Status.
- CreatedAt: Data de criação.
- UpdatedAt: Data de atualização.

### Canais de Comunicação (CommunicationChannels)
- ChannelID: Identificador único.
- ClientID: Referência ao cliente.
- ChannelType: Tipo de canal.
- ChannelIdentifier: Identificador do canal.
- Status: Status do canal.
- CreatedAt: Data de criação.
- UpdatedAt: Data de atualização.

### Assistentes (Assistants)
- AssistantID: Identificador único.
- AssistantName: Nome do assistente.
- Specialization: Especialização.
- ImplementationReference: Referência técnica.
- CreatedAt: Data de criação.
- UpdatedAt: Data de atualização.

### Relacionamento Cliente-Assistente (ClientAssistants)
- ClientAssistantID: Identificador único.
- ClientID: Referência ao cliente.
- AssistantID: Referência ao assistente.
- CreatedAt: Data de criação.
- UpdatedAt: Data de atualização.

### Sessões (Sessions)
- SessionID: Identificador único.
- ClientID: Referência ao cliente.
- ChannelID: Referência ao canal.
- UserID: Referência ao usuário interno.
- EndUserID: Referência ao usuário-cliente.
- AssistantID: Referência ao assistente.
- LiveKitRoomID: Identificador da sala.
- StartTime: Hora de início.
- EndTime: Hora de término.

### Mensagens (Messages)
- MessageID: Identificador único.
- SessionID: Referência à sessão.
- SenderType: Tipo de remetente ('Usuário', 'Usuário-Cliente', 'Assistente').
- ContentType: Tipo de conteúdo (e.g., 'Texto', 'Áudio').
- Content: Conteúdo.
- Timestamp: Hora do envio.

### Chamadas (Calls)
- CallID: Identificador único.
- SessionID: Referência à sessão.
- CallDirection: Direção ('Inbound', 'Outbound').
- SIPTrunkID: Identificador do tronco.
- CallStatus: Status.
- StartTime: Hora de início.
- EndTime: Hora de término.
- Tarefas em Segundo Plano (BackgroundTasks)
- TaskID: Identificador único.
- SessionID: Referência à sessão.
- TaskType: Tipo de tarefa (e.g., 'ConsultaCRM').
- Status: Status.
- ResultData: Resultado.
- CreatedAt: Data de criação.
- UpdatedAt: Data de atualização.

### Eventos (Events)
- EventID: Identificador único.
- SessionID: Referência à sessão.
- EventType: Tipo de evento (e.g., 'TarefaIniciada').
- EventData: Dados adicionais.
- Timestamp: Hora do evento.

## 3. Fluxo Operacional Completo e Detalhado
### Cenário 1: Cadastro e Configuração
#### 1. Cadastro do Cliente
- API: POST /clients
```sql
INSERT INTO Clients (ClientName, AdditionalInfo, CreatedAt, UpdatedAt)
VALUES ('Imobiliária XPTO', 'Especialista em imóveis de luxo', NOW(), NOW());
```

#### 2. Configuração de Canais
- API: POST /clients/{ClientID}/channels
```sql
INSERT INTO CommunicationChannels (ClientID, ChannelType, ChannelIdentifier, Status, CreatedAt, UpdatedAt)
VALUES (1, 'WhatsApp', '+5511999999999', 'Ativo', NOW(), NOW());
```

#### 3. Registro de Usuários Internos
- API: POST /clients/{ClientID}/users
```sql
INSERT INTO ClientUsers (ClientID, UserName, UserRole, Email, PhoneNumber, Status, CreatedAt, UpdatedAt)
VALUES (1, 'João Correia', 'Corretor', 'joao@imobiliariaxpto.com', '+5511988888888', 'Ativo', NOW(), NOW());
```

### Cenário 2: Interação Multi-Camada
#### 1. Recepção de Mensagem via WhatsApp
- Webhook processa o payload:
```json
{
  "from": "+5511998765432",
  "to": "+5511999999999",
  "message": "Quais imóveis estão disponíveis no bairro X?"
}
```

```sql
INSERT INTO Messages (SessionID, SenderType, ContentType, Content, Timestamp)
VALUES (<SessionID>, 'Usuário-Cliente', 'Texto', 'Quais imóveis estão disponíveis no bairro X?', NOW());
```

#### 2. Processamento Assíncrono
##### Tarefa registrada:

```sql
INSERT INTO BackgroundTasks (SessionID, TaskType, Status, CreatedAt)
VALUES (<SessionID>, 'ConsultaCRM', 'Pendente', NOW());
```

##### Atualização de evento:

```sql 
INSERT INTO Events (SessionID, EventType, EventData, Timestamp)
VALUES (<SessionID>, 'TarefaIniciada', '{"TaskType": "ConsultaCRM"}', NOW());
```

#### Cenário 3: Chamadas de Voz (Inbound e Outbound)
##### 1. Chamada Inbound (Recebida pelo Cliente)
###### Recepção da Chamada
- Evento: O sistema recebe um webhook do SIP provider, como Twilio, com os detalhes da chamada.
Payload:
```json
{
  "callSid": "CA123456789",
  "from": "+5511987654321",
  "to": "+5511999999999",
  "direction": "inbound",
  "status": "ringing"
}
```

###### Processamento:
- Identifica o cliente a partir do número de destino (to) e busca o canal associado na tabela CommunicationChannels.

###### Registra a sessão da chamada.
- Criação de Sessão e Registro da Chamada
```sql 
SELECT ClientID, ChannelID FROM CommunicationChannels
WHERE ChannelIdentifier = '+5511999999999' AND ChannelType = 'VoiceCall';
```

```sql 
INSERT INTO Sessions (ClientID, ChannelID, StartTime)
VALUES (<ClientID>, <ChannelID>, NOW());
```

###### Registro da Chamada:

```sql 
INSERT INTO Calls (SessionID, CallDirection, SIPTrunkID, CallStatus, StartTime)
VALUES (<SessionID>, 'Inbound', 'Trunk_X', 'Ringing', NOW());
```

###### Encerramento da Chamada

####### Atualização da Chamada:

```sql
UPDATE Calls
SET CallStatus = 'Completed', EndTime = NOW()
WHERE CallID = <CallID>;
```

####### Registro de Evento:

```sql
INSERT INTO Events (SessionID, EventType, EventData, Timestamp)
VALUES (<SessionID>, 'ChamadaEncerrada', '{"CallID": "<CallID>"}', NOW());
```

##### 2. Chamada Outbound (Efetuada pelo Cliente)
###### Início da Chamada
- API: POST /clients/{ClientID}/calls
```json
{
  "to": "+5511987654321",
  "from": "+5511999999999"
}
```

###### Processamento:
- Verifica se o canal do cliente (from) está configurado.
- Registra a chamada como "Iniciada".
```sql 
SELECT ChannelID FROM CommunicationChannels
WHERE ChannelIdentifier = '+5511999999999' AND ChannelType = 'VoiceCall';
```

```sql
INSERT INTO Calls (SessionID, CallDirection, SIPTrunkID, CallStatus, StartTime)
VALUES (<SessionID>, 'Outbound', 'Trunk_X', 'Initiated', NOW());
```

###### Atualização Após Conexão

- Atualiza o Status da Chamada:

```json 
UPDATE Calls
SET CallStatus = 'In Progress'
WHERE CallID = <CallID>;
```

- Registro de Evento:

```json
INSERT INTO Events (SessionID, EventType, EventData, Timestamp)
VALUES (<SessionID>, 'ChamadaConectada', '{"CallID": "<CallID>"}', NOW());
```

- Encerramento da Chamada
Processo idêntico ao fluxo de chamada inbound.

#### Cenário 4: Processamento de Tarefas Assíncronas
##### 1. Transcrição de Áudio

###### Recepção de Áudio:

O sistema recebe um áudio enviado pelo WhatsApp ou capturado em uma chamada.
Registro da Tarefa:

```json 
INSERT INTO BackgroundTasks (SessionID, TaskType, Status, CreatedAt)
VALUES (<SessionID>, 'TranscricaoAudio', 'Pendente', NOW());
```

###### Execução da Tarefa:

O sistema processa o áudio, envia para um serviço externo de transcrição e registra o resultado.

```json
UPDATE BackgroundTasks
SET Status = 'Concluída', ResultData = '{"texto": "Transcrição do áudio..."}', UpdatedAt = NOW()
WHERE TaskID = <TaskID>;
```

###### Registro de Evento:

```json
INSERT INTO Events (SessionID, EventType, EventData, Timestamp)
VALUES (<SessionID>, 'TarefaConcluída', '{"TaskID": "<TaskID>"}', NOW());
``` 

##### 2. Consultas Externas (e.g., CRM, API de Propriedades)
###### Início da Consulta:

```sql
INSERT INTO BackgroundTasks (SessionID, TaskType, Status, CreatedAt)
VALUES (<SessionID>, 'ConsultaCRM', 'Pendente', NOW());
```

###### Execução da Consulta:

O sistema realiza a chamada à API externa, armazena os dados retornados e atualiza o status.

```sql 
UPDATE BackgroundTasks
SET Status = 'Concluída', ResultData = '{"propriedades": ["Imóvel A", "Imóvel B"]}', UpdatedAt = NOW()
WHERE TaskID = <TaskID>;
```

###### Notificação ao Assistente:

O resultado da consulta é enviado para o assistente, que responde ao usuário.

- Registro de Evento:

```sql 
INSERT INTO Events (SessionID, EventType, EventData, Timestamp)
VALUES (<SessionID>, 'ConsultaConcluída', '{"TaskID": "<TaskID>"}', NOW());
```

#### Cenário 5: Notificações e Alertas
##### 1. Notificações Proativas

- Gatilho: O sistema recebe um webhook ou evento interno (e.g., novo imóvel cadastrado no CRM).

###### Registro de Evento:

```sql
INSERT INTO Events (SessionID, EventType, EventData, Timestamp)
VALUES (NULL, 'NotificaçãoProativa', '{"mensagem": "Novo imóvel disponível!"}', NOW());
```

###### Envio de Mensagem:

A notificação é enviada via WhatsApp para usuários relevantes.

##### 2. Alertas de Sistema
###### Monitoramento:

O sistema detecta um problema (e.g., falha na consulta de API).

###### Registro do Evento:

```sql 
INSERT INTO Events (SessionID, EventType, EventData, Timestamp)
VALUES (NULL, 'AlertaSistema', '{"erro": "Falha na API do CRM"}', NOW());
```

###### Notificação Interna:

O alerta é enviado para o administrador do sistema via e-mail ou painel de monitoramento.

