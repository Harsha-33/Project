export interface User {
  id: number;
  name: string;
  email: string;
  role: 'ADMIN' | 'DOCTOR' | 'PATIENT';
  created_at?: string;
}

export interface AuthResponse {
  success: boolean;
  message: string;
  data: {
    user: User;
    token: string;
  };
}

export interface ApiResponse<T> {
  success: boolean;
  message: string;
  data: T;
}

export interface Doctor {
  doctor_id: number;
  user_id: number;
  name: string;
  email: string;
  speciality: string;
  experience: number;
  qualification: string;
  designation: string;
  phone?: string;
}

export interface Patient {
  patient_id: number;
  user_id: number;
  name: string;
  email: string;
  dob?: string;
  gender?: string;
  mobile?: string;
  address?: string;
  medical_history?: string;
}

export interface Appointment {
  appointment_id: number;
  patient_id: number;
  doctor_id: number;
  patient_name?: string;
  patient_mobile?: string;
  doctor_name?: string;
  doctor_speciality?: string;
  appointment_date: string;
  symptoms?: string;
  visit_type?: string;
  status: string;
  created_at?: string;
}

export interface Prescription {
  prescription_id: number;
  consultation_id: number;
  medicine_name: string;
  dosage: string;
  timing: string;
}

export interface MedicalTest {
  test_id: number;
  consultation_id: number;
  test_name: string;
}

export interface Consultation {
  consultation_id: number;
  appointment_id: number;
  current_symptoms: string;
  physical_examination: string;
  treatment_plan: string;
  diagnosis: string;
  prescriptions: Prescription[];
  medical_tests: MedicalTest[];
  doctor_name?: string;
  appointment_date?: string;
}

export interface DashboardStats {
  upcoming_appointments?: number;
  completed_consultations?: number;
  prescriptions?: number;
  today_appointments?: number;
  pending_requests?: number;
  total_doctors?: number;
  total_patients?: number;
  total_appointments?: number;
}

export interface DoctorAvailability {
  doctor: Doctor;
  date: string;
  occupied_slots: string[];
  available_slots: string[];
}
