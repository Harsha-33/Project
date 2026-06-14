-- WeCareForYou Database Schema
-- PostgreSQL / Supabase

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('ADMIN', 'DOCTOR', 'PATIENT')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS doctors (
    doctor_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    speciality VARCHAR(100),
    experience INTEGER,
    qualification VARCHAR(200),
    designation VARCHAR(200),
    phone VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS patients (
    patient_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    dob DATE,
    gender VARCHAR(20),
    mobile VARCHAR(20),
    address VARCHAR(255),
    medical_history TEXT
);

CREATE TABLE IF NOT EXISTS appointments (
    appointment_id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(patient_id) ON DELETE CASCADE,
    doctor_id INTEGER NOT NULL REFERENCES doctors(doctor_id) ON DELETE CASCADE,
    appointment_date TIMESTAMP NOT NULL,
    symptoms TEXT,
    visit_type VARCHAR(100),
    status VARCHAR(50) DEFAULT 'PENDING' CHECK (status IN ('PENDING', 'CONFIRMED', 'ACCEPTED', 'REJECTED', 'CANCELLED', 'COMPLETED')),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX IF NOT EXISTS uq_active_doctor_slot
ON appointments (doctor_id, appointment_date)
WHERE status IN ('PENDING', 'ACCEPTED');

CREATE TABLE IF NOT EXISTS consultations (
    consultation_id SERIAL PRIMARY KEY,
    appointment_id INTEGER NOT NULL REFERENCES appointments(appointment_id) ON DELETE CASCADE,
    current_symptoms TEXT,
    physical_examination TEXT,
    treatment_plan TEXT,
    diagnosis TEXT
);

CREATE TABLE IF NOT EXISTS prescriptions (
    prescription_id SERIAL PRIMARY KEY,
    consultation_id INTEGER NOT NULL REFERENCES consultations(consultation_id) ON DELETE CASCADE,
    medicine_name VARCHAR(200) NOT NULL,
    dosage VARCHAR(50),
    timing VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS medical_tests (
    test_id SERIAL PRIMARY KEY,
    consultation_id INTEGER NOT NULL REFERENCES consultations(consultation_id) ON DELETE CASCADE,
    test_name VARCHAR(200) NOT NULL
);
