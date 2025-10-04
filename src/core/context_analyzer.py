from typing import List, Dict, Any, Optional, Tuple
from langchain.schema import BaseMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import re
import json
import os
from models.schemas import ChatMessage, UserInfo, TeachingStyle, EmotionalState

class ContextAnalyzer:
    """Analyzes conversation context to determine educational intent and extract parameters."""
    
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
        self.intent_prompt = self._create_intent_prompt()
        self.parameter_prompt = self._create_parameter_prompt()
    
    def _create_intent_prompt(self) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages([
            ("system", """You are an educational intent analyzer. Analyze the conversation to determine:
1. What educational tools are needed (note_maker, flashcard_generator, concept_explainer)
2. The primary educational intent (learning, practicing, reviewing, explaining)
3. Key topics and subjects mentioned
4. Difficulty level indicators
5. Learning preferences expressed

Return a JSON object with:
- tools_needed: list of tool names
- intent: primary educational intent
- topics: list of topics mentioned
- subject: academic subject
- difficulty_indicators: list of phrases indicating difficulty level
- confidence_score: 0-1 score for analysis confidence"""),
            ("human", "Chat History:\n{chat_history}\n\nCurrent Message: {current_message}\n\nStudent Info: {user_info}")
        ])
    
    def _create_parameter_prompt(self) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages([
            ("system", """You are a parameter extraction specialist. Extract specific parameters for educational tools from the conversation.

For each tool, extract these parameters:

NOTE_MAKER:
- topic: main subject for notes
- subject: academic discipline  
- note_taking_style: outline|bullet_points|narrative|structured
- include_examples: boolean
- include_analogies: boolean

FLASHCARD_GENERATOR:
- topic: topic for flashcards
- count: number of flashcards (1-20)
- difficulty: easy|medium|hard
- subject: academic discipline
- include_examples: boolean

CONCEPT_EXPLAINER:
- concept_to_explain: specific concept
- current_topic: broader topic context
- desired_depth: basic|intermediate|advanced|comprehensive

Use intelligent inference for missing parameters based on:
- Student's mastery level (extract from user_info)
- Emotional state (extract from user_info)
- Conversation context
- Grade level appropriateness

Return JSON with extracted parameters for each tool."""),
            ("human", "Tools Needed: {tools_needed}\n\nChat History:\n{chat_history}\n\nCurrent Message: {current_message}\n\nStudent Info: {user_info}")
        ])
    
    async def analyze_intent(self, chat_history: List[ChatMessage], current_message: str, user_info: UserInfo) -> Dict[str, Any]:
        """Analyze conversation to determine educational intent and required tools."""
        
        formatted_history = "\n".join([f"{msg.role}: {msg.content}" for msg in chat_history])
        user_info_str = f"""
        Name: {user_info.name}
        Grade: {user_info.grade_level}
        Learning Style: {user_info.learning_style_summary}
        Emotional State: {user_info.emotional_state_summary}
        Mastery Level: {user_info.mastery_level_summary}
        """
        
        try:
            response = await self.llm.ainvoke(
                self.intent_prompt.format_messages(
                    chat_history=formatted_history,
                    current_message=current_message,
                    user_info=user_info_str
                )
            )
            
            # Try to extract JSON from response
            content = response.content.strip()
            
            # Look for JSON in the response
            if content.startswith('{') and content.endswith('}'):
                result = json.loads(content)
                return result
            else:
                # Try to find JSON within the response
                import re
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    result = json.loads(json_match.group())
                    return result
                else:
                    raise ValueError("No valid JSON found in response")
            
        except Exception as e:
            print(f"Intent analysis failed, using fallback: {str(e)}")
            # Fallback analysis using keyword matching
            return self._fallback_intent_analysis(current_message, user_info)
    
    async def extract_parameters(self, tools_needed: List[str], chat_history: List[ChatMessage], 
                               current_message: str, user_info: UserInfo) -> Dict[str, Dict[str, Any]]:
        """Extract specific parameters for each required tool."""
        
        formatted_history = "\n".join([f"{msg.role}: {msg.content}" for msg in chat_history])
        user_info_str = f"""
        Name: {user_info.name}
        Grade: {user_info.grade_level}
        Learning Style: {user_info.learning_style_summary}
        Emotional State: {user_info.emotional_state_summary}
        Mastery Level: {user_info.mastery_level_summary}
        """
        
        try:
            response = await self.llm.ainvoke(
                self.parameter_prompt.format_messages(
                    tools_needed=", ".join(tools_needed),
                    chat_history=formatted_history,
                    current_message=current_message,
                    user_info=user_info_str
                )
            )
            
            # Try to extract JSON from response
            content = response.content.strip()
            
            # Look for JSON in the response
            if content.startswith('{') and content.endswith('}'):
                result = json.loads(content)
            else:
                # Try to find JSON within the response
                import re
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    result = json.loads(json_match.group())
                else:
                    raise ValueError("No valid JSON found in response")
            
            # Ensure we return tool parameters, not analysis results
            if isinstance(result, dict) and any(tool in result for tool in tools_needed):
                return result
            else:
                # If LLM didn't return proper tool parameters, use fallback
                return self._fallback_parameter_extraction(tools_needed, current_message, user_info)
            
        except Exception as e:
            print(f"Parameter extraction failed, using fallback: {str(e)}")
            # Fallback parameter extraction
            return self._fallback_parameter_extraction(tools_needed, current_message, user_info)
    
    def _fallback_intent_analysis(self, message: str, user_info: UserInfo) -> Dict[str, Any]:
        """Fallback intent analysis using keyword matching."""
        message_lower = message.lower()
        
        tools_needed = []
        
        # Simple keyword matching for tool selection
        if any(word in message_lower for word in ["notes", "note", "summary", "outline"]):
            tools_needed.append("note_maker")
        
        if any(word in message_lower for word in ["flashcard", "flash card", "memorize", "review", "quiz"]):
            tools_needed.append("flashcard_generator")
        
        if any(word in message_lower for word in ["explain", "what is", "how does", "understand", "confused"]):
            tools_needed.append("concept_explainer")
        
        # Default to concept explainer if no specific tool identified
        if not tools_needed:
            tools_needed.append("concept_explainer")
        
        return {
            "tools_needed": tools_needed,
            "intent": "learning",
            "topics": self._extract_topics(message),
            "subject": self._infer_subject(message),
            "difficulty_indicators": self._extract_difficulty_indicators(message),
            "confidence_score": 0.6
        }
    
    def _fallback_parameter_extraction(self, tools_needed: List[str], message: str, user_info: UserInfo) -> Dict[str, Dict[str, Any]]:
        """Enhanced fallback parameter extraction using improved heuristics."""
        result = {}
        
        # Use enhanced topic and subject extraction
        topics = self._extract_topics_enhanced(message)
        subject = self._infer_subject_enhanced(message)
        difficulty = self._infer_difficulty(message, user_info)
        
        # Better topic selection for flashcards
        main_topic = self._extract_main_topic_for_tool(message, topics, subject)
        
        for tool in tools_needed:
            if tool == "note_maker":
                result[tool] = {
                    "topic": main_topic,
                    "subject": subject,
                    "note_taking_style": "outline",
                    "include_examples": True,
                    "include_analogies": "visual" in user_info.learning_style_summary.lower()
                }
            
            elif tool == "flashcard_generator":
                result[tool] = {
                    "topic": main_topic,
                    "count": 7,  # Increased default count
                    "difficulty": difficulty,
                    "subject": subject,
                    "include_examples": True
                }
            
            elif tool == "concept_explainer":
                # Better concept extraction for quantum mechanics example
                concept = self._extract_main_concept(message, topics)
                result[tool] = {
                    "concept_to_explain": concept,
                    "current_topic": subject,
                    "desired_depth": "basic" if "confused" in user_info.emotional_state_summary.lower() else "intermediate"
                }
        
        return result
    
    def _extract_main_topic_for_tool(self, message: str, topics: List[str], subject: str) -> str:
        """Extract the main topic for educational tools."""
        message_lower = message.lower()
        
        # For language learning, combine subject + vocabulary/words
        if subject in ["spanish", "french", "german", "english"]:
            if "vocabulary" in message_lower or "words" in message_lower:
                return f"{subject} vocabulary"
            elif "grammar" in message_lower:
                return f"{subject} grammar"
            else:
                return f"{subject} language"
        
        # Use the first topic if available
        if topics:
            return topics[0]
        
        # Extract from common patterns
        import re
        
        # Pattern: "flashcards for X"
        for_pattern = re.search(r"(?:flashcards?|notes?|help)\s+(?:for|with|on)\s+([^.!?]+)", message_lower)
        if for_pattern:
            topic = for_pattern.group(1).strip()
            # Clean up common words
            topic = re.sub(r'\b(the|a|an|and|or|but|in|on|at|to|for|of|with|by|my|your)\b', '', topic).strip()
            if topic:
                return topic
        
        # Pattern: "I need X"
        need_pattern = re.search(r"i need\s+(?:help with\s+)?([^.!?]+)", message_lower)
        if need_pattern:
            topic = need_pattern.group(1).strip()
            topic = re.sub(r'\b(the|a|an|and|or|but|in|on|at|to|for|of|with|by|my|your)\b', '', topic).strip()
            if topic:
                return topic
        
        # Default based on subject
        if subject != "general":
            return f"{subject} concepts"
        
        return "General Study"
    
    def _extract_topics_enhanced(self, message: str) -> List[str]:
        """Enhanced topic extraction with better pattern recognition."""
        topics = []
        message_lower = message.lower()
        
        # Language-specific patterns
        language_patterns = [
            r"spanish vocabulary", r"french vocabulary", r"german vocabulary",
            r"spanish words", r"french words", r"german words",
            r"spanish language", r"french language", r"german language"
        ]
        
        # Check for language learning patterns first
        import re
        for pattern in language_patterns:
            if re.search(pattern, message_lower):
                topics.append(pattern.replace(r"\s+", " "))
        
        # Common educational concepts
        educational_concepts = [
            "quantum mechanics", "photosynthesis", "derivatives", "calculus",
            "algebra", "geometry", "evolution", "dna", "atoms", "molecules",
            "thermodynamics", "electromagnetism", "organic chemistry",
            "world war", "civil rights", "renaissance", "industrial revolution",
            "p block elements", "s block elements", "d block elements", "f block elements",
            "periodic table", "chemical bonding", "atomic structure", "electron configuration",
            "oxidation states", "ionic compounds", "covalent compounds", "molecular geometry",
            "spanish vocabulary", "french vocabulary", "german vocabulary", "english grammar",
            "math problems", "science concepts", "history facts", "literature analysis"
        ]
        
        # Check for multi-word concepts
        for concept in educational_concepts:
            if concept in message_lower and concept not in [t.lower() for t in topics]:
                topics.append(concept)
        
        # Extract subject + topic combinations
        subject_topic_patterns = [
            r"(spanish|french|german|english|math|science|history|biology|chemistry|physics)\s+(vocabulary|words|grammar|concepts|problems|facts)",
            r"(calculus|algebra|geometry)\s+(derivatives|problems|equations)",
            r"(quantum|organic|physical)\s+(mechanics|chemistry|science)"
        ]
        
        for pattern in subject_topic_patterns:
            matches = re.findall(pattern, message_lower)
            for match in matches:
                topic = " ".join(match)
                if topic not in [t.lower() for t in topics]:
                    topics.append(topic)
        
        # If no specific topics found, look for general subjects
        if not topics:
            words = message.split()
            for word in words:
                if len(word) > 3 and word.isalpha():
                    word_lower = word.lower()
                    if word_lower in ["spanish", "french", "german", "english", "math", "science", "history", "biology", "chemistry", "physics"]:
                        topics.append(word_lower)
                    elif word[0].isupper() and word_lower not in [t.lower() for t in topics]:
                        topics.append(word_lower)
        
        return topics[:3]  # Return top 3 topics
    
    def _infer_subject_enhanced(self, message: str) -> str:
        """Enhanced subject inference with better keyword matching."""
        message_lower = message.lower()
        
        # Enhanced subject keywords with language learning
        subject_keywords = {
            "spanish": ["spanish", "español", "castellano", "hispanic", "latino"],
            "french": ["french", "français", "francais", "francophone"],
            "german": ["german", "deutsch", "germanic"],
            "english": ["english", "grammar", "literature", "writing", "reading"],
            "physics": ["quantum", "mechanics", "relativity", "thermodynamics", "electromagnetism", "physics", "particle", "wave", "energy", "force"],
            "chemistry": ["molecule", "compound", "reaction", "chemistry", "chemical", "bond", "element", "acid", "base", "organic"],
            "biology": ["biology", "cell", "dna", "gene", "evolution", "organism", "photosynthesis", "respiration", "protein", "enzyme"],
            "mathematics": ["math", "algebra", "calculus", "geometry", "derivative", "integral", "equation", "function", "theorem"],
            "history": ["history", "war", "revolution", "ancient", "civilization", "empire", "battle", "treaty"],
            "literature": ["literature", "novel", "poem", "author", "character", "plot", "theme", "metaphor"]
        }
        
        # Score each subject
        subject_scores = {}
        for subject, keywords in subject_keywords.items():
            score = sum(1 for keyword in keywords if keyword in message_lower)
            if score > 0:
                subject_scores[subject] = score
        
        if subject_scores:
            return max(subject_scores, key=subject_scores.get)
        
        return "general"
    
    def _extract_main_concept(self, message: str, topics: List[str]) -> str:
        """Extract the main concept from message and topics."""
        message_lower = message.lower()
        
        # If we have topics, use the first one
        if topics:
            return topics[0]
        
        # Look for explanation requests
        explain_patterns = [
            r"explain (.+?)(?:\s|$)",
            r"what is (.+?)(?:\s|$|\?)",
            r"how does (.+?)(?:\s|$|\?)",
            r"tell me about (.+?)(?:\s|$|\?)"
        ]
        
        for pattern in explain_patterns:
            match = re.search(pattern, message_lower)
            if match:
                concept = match.group(1).strip()
                # Clean up common words
                concept = re.sub(r'\b(the|a|an|and|or|but|in|on|at|to|for|of|with|by)\b', '', concept).strip()
                if concept:
                    return concept
        
        return "the requested concept"
    
    def _extract_topics(self, message: str) -> List[str]:
        """Extract potential topics from message using simple heuristics."""
        # This is a simplified implementation - in production, use NER
        topics = []
        
        # Look for capitalized words that might be topics
        words = message.split()
        for word in words:
            if word[0].isupper() and len(word) > 3 and word.isalpha():
                topics.append(word.lower())
        
        return topics[:3]  # Return top 3 topics
    
    def _infer_subject(self, message: str) -> str:
        """Infer academic subject from message content."""
        message_lower = message.lower()
        
        subject_keywords = {
            "math": ["math", "algebra", "calculus", "geometry", "equation", "derivative"],
            "science": ["science", "biology", "chemistry", "physics", "photosynthesis", "molecule"],
            "history": ["history", "war", "revolution", "ancient", "civilization"],
            "english": ["english", "literature", "writing", "essay", "grammar"],
            "geography": ["geography", "country", "continent", "climate", "map"]
        }
        
        for subject, keywords in subject_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                return subject
        
        return "general"
    
    def _infer_difficulty(self, message: str, user_info: UserInfo) -> str:
        """Infer difficulty level from message and user context."""
        message_lower = message.lower()
        
        # Check for explicit difficulty indicators
        if any(word in message_lower for word in ["struggling", "confused", "difficult", "hard"]):
            return "easy"
        elif any(word in message_lower for word in ["challenge", "advanced", "complex"]):
            return "hard"
        
        # Infer from mastery level
        mastery_lower = user_info.mastery_level_summary.lower()
        if any(level in mastery_lower for level in ["level 1", "level 2", "level 3", "foundation"]):
            return "easy"
        elif any(level in mastery_lower for level in ["level 7", "level 8", "level 9", "level 10", "advanced"]):
            return "hard"
        
        return "medium"
    
    def _extract_difficulty_indicators(self, message: str) -> List[str]:
        """Extract phrases that indicate difficulty level."""
        indicators = []
        message_lower = message.lower()
        
        difficulty_phrases = [
            "struggling with", "confused about", "don't understand", "having trouble",
            "need help with", "challenging", "difficult", "easy", "simple", "basic"
        ]
        
        for phrase in difficulty_phrases:
            if phrase in message_lower:
                indicators.append(phrase)
        
        return indicators