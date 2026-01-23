import ai_service as ai

print("=== Testing AI Service ===")

test_text = "manholes open everywhere near my house, kids can fall, nobody fixed it"

print("\n1️⃣ Testing structure_grievance()")
structured = ai.structure_grievance(test_text)
print(structured)

print("\n2️⃣ Testing classify_department()")
dept = ai.classify_department(test_text)
print("Department:", dept)

print("\n3️⃣ Testing assign_priority()")
priority = ai.assign_priority(test_text)
print("Priority:", priority)
