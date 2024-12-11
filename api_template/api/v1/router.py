from fastapi import APIRouter

from api_template.config.versioning import APIVersion

from .controllers import (
    user_controller,
    assistant_controller,
    task_controller,
    call_controller,
    client_controller,
    client_user_controller,
    message_controller,
    communication_controller,
    event_controller
)


router = APIRouter(prefix=f"/api/{APIVersion.V1}")

router.include_router(user_controller.router, tags=["Users"])
router.include_router(assistant_controller.router, tags=["Assistants"])
router.include_router(task_controller.router, tags=["Tasks"])
router.include_router(call_controller.router, tags=["Calls"])
router.include_router(client_controller.router, tags=["Clients"])
router.include_router(client_user_controller.router, tags=["Client Users"])
router.include_router(message_controller.router, tags=["Messages"])
router.include_router(communication_controller.router, tags=["Communications"])
router.include_router(event_controller.router, tags=["Events"])
