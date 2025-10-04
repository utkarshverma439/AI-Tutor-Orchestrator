"""
Mock Educational Tools Service
Provides realistic responses for educational tools until real APIs are available.
"""

import asyncio
import random
from typing import Dict, Any, List
from datetime import datetime
from models.schemas import UserInfo, ChatMessage, ToolResponse

class MockEducationalTools:
    """Mock service that simulates educational tool responses."""
    
    def __init__(self):
        self.response_delay = 1.0  # Simulate API response time
        
    async def execute_note_maker(self, params: Dict[str, Any], user_info: UserInfo) -> ToolResponse:
        """Mock Note Maker tool execution."""
        
        await asyncio.sleep(self.response_delay)
        
        topic = params.get("topic", "General Topic")
        subject = params.get("subject", "General")
        note_style = params.get("note_taking_style", "outline")
        include_examples = params.get("include_examples", True)
        include_analogies = params.get("include_analogies", False)
        
        # Generate realistic note content based on topic
        note_content = self._generate_note_content(topic, subject, note_style, include_examples, include_analogies, user_info)
        
        return ToolResponse(
            success=True,
            tool_name="note_maker",
            data=note_content
        )
    
    async def execute_flashcard_generator(self, params: Dict[str, Any], user_info: UserInfo) -> ToolResponse:
        """Mock Flashcard Generator tool execution."""
        
        await asyncio.sleep(self.response_delay)
        
        topic = params.get("topic", "General Topic")
        count = params.get("count", 5)
        difficulty = params.get("difficulty", "medium")
        subject = params.get("subject", "General")
        include_examples = params.get("include_examples", True)
        
        # Generate realistic flashcards
        flashcards = self._generate_flashcards(topic, subject, count, difficulty, include_examples, user_info)
        
        return ToolResponse(
            success=True,
            tool_name="flashcard_generator",
            data={
                "flashcards": flashcards,
                "topic": topic,
                "difficulty": difficulty,
                "adaptation_details": f"Adapted for {user_info.learning_style_summary.split(',')[0]} and {user_info.emotional_state_summary.split(',')[0]}"
            }
        )
    
    async def execute_concept_explainer(self, params: Dict[str, Any], user_info: UserInfo) -> ToolResponse:
        """Mock Concept Explainer tool execution."""
        
        await asyncio.sleep(self.response_delay)
        
        concept = params.get("concept_to_explain", "General Concept")
        topic = params.get("current_topic", "General")
        depth = params.get("desired_depth", "intermediate")
        
        # Generate realistic explanation
        explanation_content = self._generate_explanation(concept, topic, depth, user_info)
        
        return ToolResponse(
            success=True,
            tool_name="concept_explainer",
            data=explanation_content
        )
    
    def _generate_note_content(self, topic: str, subject: str, style: str, examples: bool, analogies: bool, user_info: UserInfo) -> Dict[str, Any]:
        """Generate realistic note content."""
        
        # Topic-specific content templates
        content_templates = {
            "photosynthesis": {
                "title": "Photosynthesis: Converting Light to Energy",
                "summary": "The process by which plants convert sunlight, carbon dioxide, and water into glucose and oxygen.",
                "sections": [
                    {
                        "title": "Light-Dependent Reactions",
                        "content": "Occur in the thylakoids of chloroplasts. Chlorophyll absorbs light energy and converts it to chemical energy (ATP and NADPH).",
                        "key_points": ["Occurs in thylakoids", "Produces ATP and NADPH", "Releases oxygen as byproduct"],
                        "examples": ["Chlorophyll a and b absorption", "Photosystem I and II"] if examples else [],
                        "analogies": ["Like solar panels converting sunlight to electricity"] if analogies else []
                    },
                    {
                        "title": "Light-Independent Reactions (Calvin Cycle)",
                        "content": "Occur in the stroma. Uses ATP and NADPH to convert CO2 into glucose through carbon fixation.",
                        "key_points": ["Occurs in stroma", "Uses ATP and NADPH", "Produces glucose"],
                        "examples": ["RuBisCO enzyme function", "3-carbon and 6-carbon compounds"] if examples else [],
                        "analogies": ["Like a factory assembly line building sugar molecules"] if analogies else []
                    }
                ]
            },
            "derivatives": {
                "title": "Calculus Derivatives: Rate of Change",
                "summary": "Derivatives measure the instantaneous rate of change of a function at any given point.",
                "sections": [
                    {
                        "title": "Basic Definition",
                        "content": "The derivative of f(x) is the limit of [f(x+h) - f(x)]/h as h approaches 0.",
                        "key_points": ["Measures instantaneous rate of change", "Slope of tangent line", "Limit definition"],
                        "examples": ["f'(x) = lim(h→0) [f(x+h) - f(x)]/h"] if examples else [],
                        "analogies": ["Like measuring speedometer reading at exact moment"] if analogies else []
                    },
                    {
                        "title": "Common Rules",
                        "content": "Power rule, product rule, quotient rule, and chain rule for finding derivatives.",
                        "key_points": ["Power rule: d/dx(x^n) = nx^(n-1)", "Product rule: (uv)' = u'v + uv'", "Chain rule: (f(g(x)))' = f'(g(x))g'(x)"],
                        "examples": ["d/dx(x³) = 3x²", "d/dx(sin(2x)) = 2cos(2x)"] if examples else [],
                        "analogies": ["Like following recipes for different types of functions"] if analogies else []
                    }
                ]
            }
        }
        
        # Get template or create generic one
        template = content_templates.get(topic.lower(), {
            "title": f"{topic.title()} - Study Notes",
            "summary": f"Comprehensive notes on {topic} for {subject} studies.",
            "sections": [
                {
                    "title": "Overview",
                    "content": f"Key concepts and principles related to {topic}.",
                    "key_points": [f"Important aspect 1 of {topic}", f"Important aspect 2 of {topic}", f"Important aspect 3 of {topic}"],
                    "examples": [f"Example 1 for {topic}", f"Example 2 for {topic}"] if examples else [],
                    "analogies": [f"Think of {topic} like..."] if analogies else []
                },
                {
                    "title": "Applications",
                    "content": f"How {topic} is applied in real-world scenarios.",
                    "key_points": [f"Application 1", f"Application 2", f"Application 3"],
                    "examples": [f"Real-world example 1", f"Real-world example 2"] if examples else [],
                    "analogies": [f"Similar to everyday experience of..."] if analogies else []
                }
            ]
        })
        
        return {
            "topic": topic,
            "title": template["title"],
            "summary": template["summary"],
            "note_sections": template["sections"],
            "key_concepts": [section["title"] for section in template["sections"]],
            "connections_to_prior_learning": [f"Builds on previous knowledge of {subject}", f"Relates to fundamental concepts in {subject}"],
            "practice_suggestions": [f"Practice problems on {topic}", f"Review related {subject} concepts", f"Create concept maps"],
            "source_references": [f"{subject} textbook Chapter on {topic}", f"Online resources for {topic}"],
            "note_taking_style": style
        }
    
    def _generate_flashcards(self, topic: str, subject: str, count: int, difficulty: str, examples: bool, user_info: UserInfo) -> List[Dict[str, Any]]:
        """Generate realistic flashcards."""
        
        # Topic-specific flashcard templates
        flashcard_templates = {
            "spanish": [
                {"question": "How do you say 'hello' in Spanish?", "answer": "Hola", "example": "¡Hola! ¿Cómo estás?"},
                {"question": "What is 'goodbye' in Spanish?", "answer": "Adiós", "example": "¡Adiós! Hasta mañana."},
                {"question": "How do you say 'please' in Spanish?", "answer": "Por favor", "example": "¿Puedes ayudarme, por favor?"},
                {"question": "What is 'thank you' in Spanish?", "answer": "Gracias", "example": "Muchas gracias por tu ayuda."},
                {"question": "How do you say 'excuse me' in Spanish?", "answer": "Disculpe", "example": "Disculpe, ¿dónde está el baño?"}
            ],
            "derivatives": [
                {"question": "What is the derivative of x²?", "answer": "2x", "example": "Using power rule: d/dx(x²) = 2x¹ = 2x"},
                {"question": "What is the power rule for derivatives?", "answer": "d/dx(xⁿ) = nxⁿ⁻¹", "example": "d/dx(x³) = 3x²"},
                {"question": "What is the derivative of sin(x)?", "answer": "cos(x)", "example": "d/dx(sin(x)) = cos(x)"},
                {"question": "What is the derivative of eˣ?", "answer": "eˣ", "example": "d/dx(eˣ) = eˣ (special property)"},
                {"question": "What is the chain rule?", "answer": "(f(g(x)))' = f'(g(x))g'(x)", "example": "d/dx(sin(2x)) = cos(2x) · 2 = 2cos(2x)"}
            ],
            "photosynthesis": [
                {"question": "What is the overall equation for photosynthesis?", "answer": "6CO₂ + 6H₂O + light → C₆H₁₂O₆ + 6O₂", "example": "Carbon dioxide + water + light energy → glucose + oxygen"},
                {"question": "Where do light-dependent reactions occur?", "answer": "Thylakoids", "example": "In the thylakoid membranes of chloroplasts"},
                {"question": "What does the Calvin cycle produce?", "answer": "Glucose (C₆H₁₂O₆)", "example": "Uses CO₂ and energy to make sugar"},
                {"question": "What pigment captures light energy?", "answer": "Chlorophyll", "example": "Chlorophyll a and b absorb different wavelengths"},
                {"question": "What are the products of light reactions?", "answer": "ATP, NADPH, and O₂", "example": "Energy carriers and oxygen gas"}
            ]
        }
        
        # Get appropriate template or create generic ones
        if topic.lower() in flashcard_templates:
            template_cards = flashcard_templates[topic.lower()]
        else:
            template_cards = [
                {"question": f"What is the main concept of {topic}?", "answer": f"Key principle of {topic}", "example": f"Example related to {topic}"},
                {"question": f"How is {topic} applied?", "answer": f"Application of {topic}", "example": f"Real-world use of {topic}"},
                {"question": f"What are the components of {topic}?", "answer": f"Parts of {topic}", "example": f"Elements that make up {topic}"},
                {"question": f"Why is {topic} important?", "answer": f"Significance of {topic}", "example": f"Impact of {topic}"},
                {"question": f"How does {topic} work?", "answer": f"Process of {topic}", "example": f"Step-by-step {topic}"}
            ]
        
        # Select and adapt cards based on count and difficulty
        selected_cards = template_cards[:min(count, len(template_cards))]
        
        # Adapt difficulty
        for card in selected_cards:
            if difficulty == "easy":
                card["question"] = card["question"].replace("What is", "What is the basic")
            elif difficulty == "hard":
                card["question"] = card["question"].replace("What is", "Analyze and explain")
        
        # Add examples if requested
        if not examples:
            for card in selected_cards:
                card.pop("example", None)
        
        return [
            {
                "title": f"{topic.title()} - Card {i+1}",
                "question": card["question"],
                "answer": card["answer"],
                "example": card.get("example", "") if examples else ""
            }
            for i, card in enumerate(selected_cards)
        ]
    
    def _generate_explanation(self, concept: str, topic: str, depth: str, user_info: UserInfo) -> Dict[str, Any]:
        """Generate realistic concept explanations."""
        
        # Concept-specific explanations
        explanations = {
            "quantum mechanics": {
                "basic": "Quantum mechanics is the science of very small things like atoms and particles. It shows that these tiny things behave very differently from the big objects we see every day.",
                "intermediate": "Quantum mechanics is a fundamental theory in physics that describes the behavior of matter and energy at the atomic and subatomic scale. It reveals that particles can exist in multiple states simultaneously and that observation affects reality.",
                "advanced": "Quantum mechanics is a mathematical framework describing the probabilistic behavior of quantum systems through wave functions, operators, and the Schrödinger equation, incorporating principles like superposition, entanglement, and wave-particle duality.",
                "comprehensive": "Quantum mechanics represents a complete theoretical framework for understanding the fundamental nature of reality at the quantum scale, incorporating advanced concepts like quantum field theory, many-worlds interpretation, and the measurement problem in quantum foundations."
            },
            "photosynthesis": {
                "basic": "Photosynthesis is how plants make food using sunlight, water, and carbon dioxide.",
                "intermediate": "Photosynthesis is a complex process where plants convert light energy into chemical energy (glucose) through two main stages: light-dependent reactions and the Calvin cycle.",
                "advanced": "Photosynthesis involves intricate biochemical pathways including photosystem complexes, electron transport chains, and carbon fixation mechanisms that convert electromagnetic radiation into stored chemical energy.",
                "comprehensive": "Photosynthesis represents a fundamental energy conversion process involving quantum mechanical light absorption, redox chemistry, and metabolic regulation that sustains virtually all life on Earth through primary productivity."
            },
            "derivatives": {
                "basic": "A derivative tells you how fast something is changing at any moment.",
                "intermediate": "A derivative measures the instantaneous rate of change of a function, representing the slope of the tangent line at any point.",
                "advanced": "Derivatives are linear operators that quantify local rates of change through limit processes, forming the foundation of differential calculus and optimization theory.",
                "comprehensive": "Derivatives represent the fundamental concept of local linearity in analysis, providing the mathematical framework for understanding dynamic systems, optimization, and the geometric properties of manifolds."
            },
            "atoms": {
                "basic": "Atoms are tiny building blocks that make up everything around us.",
                "intermediate": "Atoms are the smallest units of matter that retain the properties of an element, consisting of protons, neutrons, and electrons.",
                "advanced": "Atoms are quantum mechanical systems where electrons exist in probability distributions around nuclei, governed by the Schrödinger equation and quantum numbers.",
                "comprehensive": "Atoms represent discrete quantum systems exhibiting wave-particle duality, with electronic structure determined by solutions to the many-body Schrödinger equation in the context of quantum field theory."
            },
            "p block elements": {
                "basic": "P block elements are found on the right side of the periodic table and include groups 13-18. They have their outermost electrons in p orbitals.",
                "intermediate": "P block elements include metals, metalloids, and nonmetals with diverse properties. Their electron configuration ends in p¹ to p⁶, giving them varied chemical behaviors from reactive halogens to inert noble gases.",
                "advanced": "P block elements exhibit complex bonding patterns due to the directional nature of p orbitals, leading to phenomena like hybridization, multiple oxidation states, and the formation of both ionic and covalent compounds with diverse geometries.",
                "comprehensive": "P block elements demonstrate the full spectrum of chemical bonding theory, from the electron-deficient bonding in boron compounds to the hypervalency in phosphorus and sulfur, illustrating advanced concepts in molecular orbital theory and VSEPR geometry."
            },
            "periodic table": {
                "basic": "The periodic table organizes all chemical elements by their properties and atomic structure.",
                "intermediate": "The periodic table arranges elements by increasing atomic number, showing periodic trends in properties like atomic size, ionization energy, and electronegativity.",
                "advanced": "The periodic table reflects the quantum mechanical structure of atoms, with periods corresponding to electron shells and groups reflecting similar valence electron configurations and chemical properties.",
                "comprehensive": "The periodic table embodies the fundamental principles of quantum chemistry, demonstrating how electron configuration determines chemical behavior through concepts like effective nuclear charge, orbital penetration, and relativistic effects in heavy elements."
            }
        }
        
        # Get explanation with better matching
        concept_lower = concept.lower().strip()
        
        # Try exact match first
        if concept_lower in explanations:
            explanation_text = explanations[concept_lower].get(depth, explanations[concept_lower]["intermediate"])
        else:
            # Try partial matching for compound concepts
            matched_explanation = None
            for key in explanations.keys():
                if key in concept_lower or concept_lower in key:
                    matched_explanation = explanations[key]
                    break
            
            if matched_explanation:
                explanation_text = matched_explanation.get(depth, matched_explanation["intermediate"])
            else:
                # Generate contextual explanation
                depth_templates = {
                    "basic": f"{concept} is a fundamental concept in {topic}. It involves key principles that are important to understand.",
                    "intermediate": f"{concept} involves several key principles and mechanisms that are important in {topic}. Understanding this concept requires grasping its main components and how they work together.",
                    "advanced": f"{concept} represents a complex system with multiple interacting components and theoretical frameworks in {topic}. It requires deep understanding of underlying principles.",
                    "comprehensive": f"{concept} encompasses sophisticated theoretical and practical aspects that form the foundation of advanced {topic} studies. It connects to many other concepts in the field."
                }
                explanation_text = depth_templates.get(depth, depth_templates["intermediate"])
        
        # Generate topic-specific content
        examples, related_concepts, practice_questions = self._generate_topic_specific_content(concept_lower, topic)
        
        visual_aids = [
            f"Diagram showing {concept} process",
            f"Chart illustrating {concept} relationships",
            f"Graph depicting {concept} changes"
        ]
        
        return {
            "explanation": explanation_text,
            "examples": examples,
            "related_concepts": related_concepts,
            "visual_aids": visual_aids,
            "practice_questions": practice_questions,
            "source_references": [f"{topic} textbook", f"Academic papers on {concept}", f"Online resources for {concept}"]
        }
    
    def _generate_topic_specific_content(self, concept: str, topic: str) -> tuple[list, list, list]:
        """Generate topic-specific examples, related concepts, and practice questions."""
        
        # Topic-specific content database
        content_database = {
            "quantum mechanics": {
                "examples": [
                    "Electron tunneling in quantum devices like tunnel diodes",
                    "Superposition in quantum computers using qubits",
                    "Wave-particle duality demonstrated in double-slit experiments"
                ],
                "related_concepts": [
                    "Wave-particle duality",
                    "Heisenberg uncertainty principle", 
                    "Schrödinger equation"
                ],
                "practice_questions": [
                    "How does quantum superposition enable quantum computing?",
                    "What role does observation play in quantum measurement?",
                    "How do quantum tunneling effects work in modern electronics?"
                ]
            },
            "photosynthesis": {
                "examples": [
                    "Light reactions in chloroplasts converting sunlight to ATP",
                    "Calvin cycle fixing CO₂ into glucose in plant leaves",
                    "Oxygen production as a byproduct in aquatic plants"
                ],
                "related_concepts": [
                    "Cellular respiration",
                    "Chlorophyll and light absorption",
                    "Carbon fixation pathways"
                ],
                "practice_questions": [
                    "How do light and dark reactions work together in photosynthesis?",
                    "What factors can limit the rate of photosynthesis?",
                    "How does photosynthesis contribute to the global carbon cycle?"
                ]
            },
            "p block elements": {
                "examples": [
                    "Halogens like chlorine used in water purification",
                    "Noble gases like helium used in balloons and diving",
                    "Carbon forming diverse compounds in organic chemistry"
                ],
                "related_concepts": [
                    "Periodic trends in p block",
                    "Electronegativity and ionization energy",
                    "Chemical bonding patterns"
                ],
                "practice_questions": [
                    "How do p block elements show variable oxidation states?",
                    "What makes noble gases chemically inert?",
                    "How does electronegativity change across p block groups?"
                ]
            },
            "derivatives": {
                "examples": [
                    "Velocity as the derivative of position with respect to time",
                    "Marginal cost in economics as derivative of total cost",
                    "Slope of tangent lines to curves at specific points"
                ],
                "related_concepts": [
                    "Limits and continuity",
                    "Integration (antiderivatives)",
                    "Chain rule and product rule"
                ],
                "practice_questions": [
                    "How do you find the derivative of composite functions?",
                    "What is the relationship between derivatives and rates of change?",
                    "How are derivatives used in optimization problems?"
                ]
            }
        }
        
        # Get specific content or generate generic fallback
        if concept in content_database:
            content = content_database[concept]
            return content["examples"], content["related_concepts"], content["practice_questions"]
        else:
            # Generic fallback
            examples = [
                f"Practical application of {concept} in real-world scenarios",
                f"Laboratory demonstration showing {concept} principles",
                f"Industrial or technological use of {concept}"
            ]
            related_concepts = [
                f"Fundamental principles underlying {concept}",
                f"Advanced applications of {concept}",
                f"Historical development of {concept}"
            ]
            practice_questions = [
                f"What are the key principles of {concept}?",
                f"How is {concept} applied in practice?",
                f"What are the implications of {concept}?"
            ]
            return examples, related_concepts, practice_questions

# Global instance
mock_tools = MockEducationalTools()