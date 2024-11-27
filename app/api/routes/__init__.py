from fastapi import APIRouter

# Routes Import
from .example_routes import router as example_router, get_tag_description as example_tag_description
from .auth_routes import router as auth_router, get_tag_description as auth_tag_description

__version__ = 1.0

router = APIRouter(
    prefix='/v1'
)

router.include_router(example_router) # Adding a route to project
router.include_router(auth_router)

def get_tags_description():
    tags = []
    tags.append(example_tag_description()) # Adding a documentation tag from a specific router to project
    tags.append(auth_tag_description())
    return tags
