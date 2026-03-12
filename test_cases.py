TEST_CASES = {
    "summarization": [
        {
            "id": "sum_1",
            "input": "The United Nations was established in 1945 after World War II to prevent future conflicts. It has 193 member states and works on issues including peace, security, human rights, and development. The UN headquarters is in New York City. Key bodies include the General Assembly, Security Council, and International Court of Justice.",
            "expected_keywords": ["1945", "193", "peace", "security", "New York"],
            "task": "Summarize this text in 2-3 sentences"
        },
        {
            "id": "sum_2",
            "input": "Machine learning is a subset of artificial intelligence that enables systems to learn from data without being explicitly programmed. It uses algorithms to identify patterns in data and make predictions. Common types include supervised learning, unsupervised learning, and reinforcement learning.",
            "expected_keywords": ["artificial intelligence", "algorithms", "patterns", "supervised", "data"],
            "task": "Summarize this text in 2-3 sentences"
        },
        {
            "id": "sum_3",
            "input": "The Indian Space Research Organisation ISRO successfully landed Chandrayaan-3 on the lunar south pole on August 23 2023. This made India the fourth country to land on the Moon and the first to land near the south pole. The mission cost approximately 615 crore rupees.",
            "expected_keywords": ["ISRO", "Chandrayaan-3", "south pole", "2023", "fourth"],
            "task": "Summarize this text in 2-3 sentences"
        }
    ],
    "classification": [
        {
            "id": "cls_1",
            "input": "I absolutely love this product! Best purchase I have ever made.",
            "expected_answer": "positive",
            "task": "Classify this review as positive, negative, or neutral. Reply with one word only."
        },
        {
            "id": "cls_2",
            "input": "Terrible experience. Product broke within 2 days. Complete waste of money.",
            "expected_answer": "negative",
            "task": "Classify this review as positive, negative, or neutral. Reply with one word only."
        },
        {
            "id": "cls_3",
            "input": "The product is okay. Nothing special but works as expected.",
            "expected_answer": "neutral",
            "task": "Classify this review as positive, negative, or neutral. Reply with one word only."
        },
        {
            "id": "cls_4",
            "input": "This is the worst restaurant I have ever been to. Cold food and rude staff.",
            "expected_answer": "negative",
            "task": "Classify this review as positive, negative, or neutral. Reply with one word only."
        },
        {
            "id": "cls_5",
            "input": "Outstanding service! The team went above and beyond. Highly recommend.",
            "expected_answer": "positive",
            "task": "Classify this review as positive, negative, or neutral. Reply with one word only."
        }
    ],
    "extraction": [
        {
            "id": "ext_1",
            "input": "John Smith is a 35-year-old software engineer at Google in San Francisco. He graduated from MIT in 2013. His email is john@gmail.com.",
            "expected_keywords": ["John Smith", "35", "Google", "San Francisco", "MIT", "2013"],
            "task": "Extract all entities: name, age, company, location, education, contact"
        },
        {
            "id": "ext_2",
            "input": "Tesla Inc reported revenue of 25.2 billion dollars in Q3 2024. CEO Elon Musk announced plans to launch 3 new models by 2026. Headquarters in Austin Texas.",
            "expected_keywords": ["Tesla", "25.2", "Q3 2024", "Elon Musk", "Austin"],
            "task": "Extract: company, revenue, quarter, CEO, headquarters, future plans"
        }
    ],
    "reasoning": [
        {
            "id": "rea_1",
            "input": "If all roses are flowers, and all flowers need water, do all roses need water?",
            "expected_answer": "yes",
            "task": "Answer with yes or no and explain briefly"
        },
        {
            "id": "rea_2",
            "input": "A train travels 120 km in 2 hours. What is its speed in km per hour?",
            "expected_answer": "60",
            "task": "Calculate and give the numerical answer"
        },
        {
            "id": "rea_3",
            "input": "If January 1st is a Monday, what day is January 15th?",
            "expected_answer": "monday",
            "task": "Calculate and give the day name"
        }
    ]
}

def get_all_test_cases():
    all_cases = []
    for category, cases in TEST_CASES.items():
        for case in cases:
            case["category"] = category
            all_cases.append(case)
    return all_cases

def get_test_cases_by_category(category):
    return TEST_CASES.get(category, [])

def get_categories():
    return list(TEST_CASES.keys())
