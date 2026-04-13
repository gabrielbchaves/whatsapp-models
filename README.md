# whatsapp-models

Biblioteca Python de modelos de dados ([Pydantic v2](https://docs.pydantic.dev/latest/)) para as APIs do WhatsApp Business da Meta.

## Instalação

```bash
pip install whatsapp-models
# ou com uv
uv add whatsapp-models
```

## Módulos

| Módulo | Descrição |
|---|---|
| `messages` | Modelos de envio (`POST /messages`) |
| `message_templates` | Criação e envio de templates |
| `webhooks` | Payloads recebidos via webhook |
| `phone_numbers` | Gerenciamento de números |
| `media` | Upload e referência de mídia |

---

## Exemplos

### Envio de mensagens

#### Mensagem de texto

```python
from whatsapp_models import TextMessage

msg = TextMessage(to="+5511999999999", text={"body": "Olá!"})
payload = msg.model_dump()
# POST /messages — body: payload
```

#### Mensagem de mídia (imagem, vídeo, documento, áudio, sticker)

```python
from whatsapp_models import ImageMessage, DocumentMessage

# Por ID de mídia previamente enviada
image = ImageMessage(to="+5511999999999", image={"id": "media_id_abc", "caption": "Foto do evento"})

# Por URL hospedada
doc = DocumentMessage(
    to="+5511999999999",
    document={"link": "https://example.com/relatorio.pdf", "filename": "relatorio.pdf"},
)
```

#### Mensagem interativa — botões de resposta rápida

```python
from whatsapp_models import InteractiveMessage

msg = InteractiveMessage(
    to="+5511999999999",
    interactive={
        "type": "button",
        "body": {"text": "Confirme sua presença:"},
        "action": {
            "buttons": [
                {"type": "reply", "reply": {"id": "sim", "title": "Sim"}},
                {"type": "reply", "reply": {"id": "nao", "title": "Não"}},
            ]
        },
    },
)
```

#### Mensagem interativa — lista

```python
from whatsapp_models import InteractiveMessage

msg = InteractiveMessage(
    to="+5511999999999",
    interactive={
        "type": "list",
        "body": {"text": "Escolha um departamento:"},
        "action": {
            "button": "Ver opções",
            "sections": [
                {
                    "title": "Suporte",
                    "rows": [
                        {"id": "tecnico", "title": "Suporte Técnico"},
                        {"id": "financeiro", "title": "Financeiro"},
                    ],
                }
            ],
        },
    },
)
```

#### Mensagem via template

```python
from whatsapp_models import TemplateMessage

msg = TemplateMessage(
    to="+5511999999999",
    template={
        "name": "hello_world",
        "language": {"code": "pt_BR"},
        "components": [
            {
                "type": "body",
                "parameters": [{"type": "text", "text": "João"}],
            }
        ],
    },
)
```

#### Discriminated union — `OutgoingMessage`

Útil para serializar ou deserializar qualquer mensagem de saída pelo campo `type`:

```python
from pydantic import TypeAdapter
from whatsapp_models import OutgoingMessage

adapter = TypeAdapter(OutgoingMessage)
msg = adapter.validate_python({
    "to": "+5511999999999",
    "type": "text",
    "text": {"body": "Olá!"},
})
# msg é uma instância de TextMessage
```

---

### Templates

#### Criação de template

```python
from whatsapp_models import (
    CreateTemplateRequest,
    TemplateCategory,
    HeaderComponent,
    BodyComponent,
    FooterComponent,
    HeaderFormat,
)

request = CreateTemplateRequest(
    name="confirmacao_pedido",
    language="pt_BR",
    category=TemplateCategory.UTILITY,
    components=[
        HeaderComponent(format=HeaderFormat.TEXT, text="Pedido confirmado"),
        BodyComponent(text="Olá {{1}}, seu pedido #{{2}} foi confirmado."),
        FooterComponent(text="Dúvidas? Fale conosco."),
    ],
)
```

---

### Webhooks

#### Deserializar notificação recebida

```python
from whatsapp_models import WebhookNotification

payload = { ... }  # dict recebido no endpoint
notification = WebhookNotification.model_validate(payload)

for entry in notification.entry:
    for change in entry.changes:
        for message in change.value.messages:
            print(type(message).__name__, message.type)
```

#### Mensagem direta — text

```python
from whatsapp_models.webhooks.messages import IncomingTextMessage

if isinstance(message, IncomingTextMessage):
    print(message.from_, message.text.body)
```

#### Mensagem de grupo

Mensagens de grupo possuem `group_id` no payload e são resolvidas automaticamente para o tipo `IncomingGroup*` correspondente:

```python
from whatsapp_models.webhooks.messages import IncomingGroupTextMessage

if isinstance(message, IncomingGroupTextMessage):
    print(f"Grupo {message.group_id}: {message.text.body}")
```

#### Status de entrega

```python
from whatsapp_models.webhooks.statuses import DeliveryStatus

for status in change.value.statuses:
    if status.status == DeliveryStatus.failed:
        print(f"Falha ao entregar {status.id}: {status.errors}")
```

---

### Números de telefone

```python
from whatsapp_models import PhoneNumber, QualityRating

pn = PhoneNumber(
    id="pn_id_1",
    display_phone_number="+55 11 99999-9999",
    verified_name="Minha Empresa",
    quality_rating=QualityRating.GREEN,
)
```

---

### Mídia

```python
from whatsapp_models import MediaObject

# Referência por ID (após upload)
ref = MediaObject(id="media_id_abc")

# Referência por URL
ref = MediaObject(link="https://example.com/audio.ogg", filename="audio.ogg")
```

---

## Convenções

- Todos os modelos herdam de `pydantic.BaseModel` com `validate_by_name=True` e `validate_by_alias=True`
- Campos opcionais usam `field: Type | None = None`
- Enums usam `StrEnum` — serializam como string pura
- Discriminated unions usam `Field(discriminator="type")` para parse direto sem tentativa e erro

## Desenvolvimento

```bash
uv sync
uv run pytest
uv run ruff check . && uv run ruff format .
```
