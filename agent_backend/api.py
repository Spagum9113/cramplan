from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
from typing import List, Dict
import logging

# Import environment setup to ensure it's loaded
import env_setup

# Import specific components from llm_main
from llm_main import (
    main_topic_outline_agent, 
    open_quiz_agent, 
    content_writer_agent,
    curated_topic_outline_agent,
    evaluate_quiz_understanding,
    Runner
)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="CramPlan API", description="API for generating learning content based on user understanding")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class TopicRequest(BaseModel):
    subject: str

class QuizAnswer(BaseModel):
    question_index: int
    answer: str

class QuizSubmission(BaseModel):
    answers: List[QuizAnswer]

class Topic(BaseModel):
    topic: str
    description: str
    subtopics: List[str]

class TopicResponse(BaseModel):
    list_of_topics: List[Topic]

class QuizQuestion(BaseModel):
    topic: str
    quiz_question: str
    choice_a: str
    choice_b: str
    choice_c: str
    choice_d: str
    correct_answer: str

class QuizResponse(BaseModel):
    list_quiz_questions: List[QuizQuestion]

class ContentSub(BaseModel):
    sub_topic_title: str
    sub_content_text: str

class ContentMain(BaseModel):
    topic_title: str
    main_description: str
    subtopics: List[ContentSub]

class ContentResponse(BaseModel):
    topic: List[ContentMain]

class UnderstandingScore(BaseModel):
    scores: Dict[str, float]

@app.post("/generate-topics", response_model=TopicResponse)
async def generate_topics(request: TopicRequest):
    try:
        logger.info(f"Generating topics for subject: {request.subject}")
        # Create an agent and generate topics
        input_prompt = request.subject

        main_topic_result = await Runner.run(
            main_topic_outline_agent,
            input_prompt,
        )
        
        logger.info(f"Generated {len(main_topic_result.final_output.list_of_topics)} topics")
        return main_topic_result.final_output
    except Exception as e:
        logger.error(f"Error generating topics: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error generating topics: {str(e)}")

@app.post("/generate-quiz", response_model=QuizResponse)
async def generate_quiz(topics: TopicResponse):
    try:
        logger.info(f"Generating quiz for {len(topics.list_of_topics)} topics")
        # Format topics into string
        topics_string = "\n".join(
            f"{i+1}. {topic.topic}\n   Description: {topic.description}\n   Subtopics: {', '.join(topic.subtopics)}" 
            for i, topic in enumerate(topics.list_of_topics)
        )
        
        # Generate quiz questions
        quiz_result = await Runner.run(
            open_quiz_agent,
            f"Here are the topics:\n{topics_string}"
        )
        logger.info(f"Generated {len(quiz_result.final_output.list_quiz_questions)} quiz questions")
        return quiz_result.final_output
    except Exception as e:
        logger.error(f"Error generating quiz: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error generating quiz: {str(e)}")

@app.post("/evaluate-quiz", response_model=UnderstandingScore)
async def evaluate_quiz(topics: TopicResponse, quiz: QuizResponse, submission: QuizSubmission):
    try:
        logger.info(f"Evaluating quiz with {len(submission.answers)} answers")
        # Convert submission format
        user_answers = [{"question_index": ans.question_index, "answer": ans.answer} 
                       for ans in submission.answers]
        
        # Evaluate quiz
        understanding_scores = evaluate_quiz_understanding(quiz, user_answers)
        logger.info(f"Evaluated understanding for {len(understanding_scores)} topics")
        return {"scores": understanding_scores}
    except Exception as e:
        logger.error(f"Error evaluating quiz: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error evaluating quiz: {str(e)}")

@app.post("/generate-content", response_model=ContentResponse)
async def generate_content(topics: TopicResponse, understanding: UnderstandingScore):
    try:
        logger.info(f"Generating content for {len(topics.list_of_topics)} topics")
        # Format topics and understanding scores
        topics_string = "\n".join(
            f"{i+1}. {topic.topic}\n   Description: {topic.description}\n   Subtopics: {', '.join(topic.subtopics)}" 
            for i, topic in enumerate(topics.list_of_topics)
        )
        understanding_summary = "\nUnderstanding by Topic:\n"
        understanding_summary += "\n".join(
            f"{topic}: {score:.1f}%" 
            for topic, score in understanding.scores.items()
        )
        
        # Generate content
        content_result = await Runner.run(
            content_writer_agent,
            f"""Here are the topics to write content for:\n{topics_string}
You need to output the main content, its description and the subtopics with the content for each subtopic."""
        )
        logger.info(f"Generated content with {len(content_result.final_output.topic)} sections")
        return content_result.final_output
    except Exception as e:
        logger.error(f"Error generating content: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error generating content: {str(e)}")

@app.post("/curate-topics", response_model=TopicResponse)
async def curate_topics(request: TopicRequest, understanding: UnderstandingScore):
    try:
        logger.info(f"Curating topics for subject: {request.subject}")
        # Format understanding scores
        understanding_string = "\n".join(
            f"{topic}: {score:.1f}%" 
            for topic, score in understanding.scores.items()
        )
        
        # Generate curated topics
        curated_result = await Runner.run(
            curated_topic_outline_agent,
            f"Here is the main topic:\n{request.subject}\nHere is the understanding of the topic:\n{understanding_string}"
        )
        
        logger.info(f"Curated {len(curated_result.final_output.list_of_topics)} topics")
        return curated_result.final_output
    except Exception as e:
        logger.error(f"Error curating topics: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error curating topics: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Example of a complete flow endpoint
@app.post("/complete-flow", response_model=Dict)
async def complete_flow(request: TopicRequest, quiz_submission: QuizSubmission):
    try:
        logger.info(f"Starting complete flow for subject: {request.subject}")
        
        # 1. Generate topics
        logger.info("Step 1: Generating topics")
        topics_result = await generate_topics(request)
        
        # 2. Generate quiz
        logger.info("Step 2: Generating quiz")
        quiz_result = await generate_quiz(topics_result)
        
        # 3. Evaluate quiz
        logger.info("Step 3: Evaluating quiz")
        understanding = await evaluate_quiz(topics_result, quiz_result, quiz_submission)
        
        # 4. Curate topics based on understanding
        logger.info("Step 4: Curating topics")
        curated_topics = await curate_topics(request, understanding)
        
        # 5. Generate content based on curated topics
        logger.info("Step 5: Generating content with detailed structure")
        content = await generate_content(curated_topics, understanding)
        
        logger.info("Complete flow finished successfully")
        # Return complete results
        return {
            "topics": topics_result,
            "quiz": quiz_result,
            "understanding": understanding,
            "curated_topics": curated_topics,
            "content": content
        }
    except Exception as e:
        logger.error(f"Error in complete flow: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error in complete flow: {str(e)}") 