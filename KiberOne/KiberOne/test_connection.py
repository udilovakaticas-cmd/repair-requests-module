from firebase_config import db

doc_ref = db.collection("users").document("student_test")
doc_ref.set({
    "name": "Test Student",
    "role": "student",
    "age": 9,
    "progress_level": 1
})

print("✅ Data successfully written to Firestore!")
