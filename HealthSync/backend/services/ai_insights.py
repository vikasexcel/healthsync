import os
import logging
from fastapi import HTTPException
from langchain import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import UserHealthData  # Assuming you have a UserHealthData model defined

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIInsightsService:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        self.llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.prompt_template = PromptTemplate(
            input_variables=["user_data"],
            template="Based on the following health data: {user_data}, generate personalized health insights."
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt_template)

    async def generate_insights(self, user_id: int):
        try:
            async with self.db_session() as session:
                result = await session.execute(select(UserHealthData).where(UserHealthData.user_id == user_id))
                user_health_data = result.scalars().first()

                if not user_health_data:
                    raise HTTPException(status_code=404, detail="User health data not found")

                insights = await self._get_insights(user_health_data)
                return insights

        except Exception as e:
            logger.error(f"Error generating insights for user {user_id}: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    async def _get_insights(self, user_health_data):
        user_data = self._format_user_data(user_health_data)
        insights = await self.chain.arun(user_data)
        return insights

    def _format_user_data(self, user_health_data):
        # Format the user health data into a string or structured format suitable for the prompt
        return f"Age: {user_health_data.age}, Weight: {user_health_data.weight}, Height: {user_health_data.height}, Conditions: {user_health_data.conditions}"

# Usage example (to be called in your FastAPI route)
# ai_insights_service = AIInsightsService(db_session)
# insights = await ai_insights_service.generate_insights(user_id)