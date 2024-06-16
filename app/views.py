from flask_smorest import Blueprint, abort
from flask.views import MethodView
from app.models import db, Story, Page
from app.schemas import StorySchema, PageSchema
from app.story_generator import generate_bullet_points, generate_story_page, extract_characters_from_illustration

blp = Blueprint("stories", __name__, url_prefix="/api/stories", description="Operations on stories")

@blp.route("/")
class StoryList(MethodView):
    @blp.arguments(StorySchema)
    @blp.response(201, StorySchema)
    def post(self, new_story_data):
        bullet_points = generate_bullet_points(new_story_data["age"], new_story_data["topic"], new_story_data["gender"])
        new_story_data["bullet_points"] = "\n".join(bullet_points)
        story = Story(**new_story_data)
        db.session.add(story)
        db.session.commit()
        return story

@blp.route("/<int:story_id>/pages")
class PageList(MethodView):
    @blp.response(200, PageSchema(many=True))
    def get(self, story_id):
        pages = Page.query.filter_by(story_id=story_id).all()
        return pages
    
    @blp.arguments(PageSchema)
    @blp.response(201, PageSchema)
    def post(self, new_page_data, story_id):
        story = Story.query.get_or_404(story_id)
        history = "\n".join([page.content for page in story.pages])
        bullet_points = story.bullet_points.split('\n')
        characters = story.characters or {}
        content, illustration = generate_story_page(bullet_points, history, characters)
        
        # Update characters with any new details from the illustration
        new_characters = extract_characters_from_illustration(illustration)
        characters.update(new_characters)
        story.characters = characters
        
        page_number = len(story.pages) + 1
        page = Page(story_id=story_id, content=content, illustration=illustration, page_number=page_number)
        db.session.add(page)
        db.session.commit()
        return page
