import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { ApiResponse, Appointment, DashboardStats, Doctor, Patient } from '../models';

@Injectable({ providedIn: 'root' })
export class AdminApiService {
  private apiUrl = `${environment.apiUrl}/admin`;

  constructor(private http: HttpClient) {}

  getDashboard(): Observable<ApiResponse<DashboardStats>> {
    return this.http.get<ApiResponse<DashboardStats>>(`${this.apiUrl}/dashboard`);
  }

  getDoctors(): Observable<ApiResponse<Doctor[]>> {
    return this.http.get<ApiResponse<Doctor[]>>(`${this.apiUrl}/doctors`);
  }

  addDoctor(data: Record<string, unknown>): Observable<ApiResponse<Doctor>> {
    return this.http.post<ApiResponse<Doctor>>(`${this.apiUrl}/doctor`, data);
  }

  updateDoctor(id: number, data: Record<string, unknown>): Observable<ApiResponse<Doctor>> {
    return this.http.put<ApiResponse<Doctor>>(`${this.apiUrl}/doctor/${id}`, data);
  }

  deleteDoctor(id: number): Observable<ApiResponse<unknown>> {
    return this.http.delete<ApiResponse<unknown>>(`${this.apiUrl}/doctor/${id}`);
  }

  getPatients(): Observable<ApiResponse<Patient[]>> {
    return this.http.get<ApiResponse<Patient[]>>(`${this.apiUrl}/patients`);
  }

  addPatient(data: Record<string, unknown>): Observable<ApiResponse<Patient>> {
    return this.http.post<ApiResponse<Patient>>(`${this.apiUrl}/patient`, data);
  }

  updatePatient(id: number, data: Record<string, unknown>): Observable<ApiResponse<Patient>> {
    return this.http.put<ApiResponse<Patient>>(`${this.apiUrl}/patient/${id}`, data);
  }

  deletePatient(id: number): Observable<ApiResponse<unknown>> {
    return this.http.delete<ApiResponse<unknown>>(`${this.apiUrl}/patient/${id}`);
  }

  getAppointments(): Observable<ApiResponse<Appointment[]>> {
    return this.http.get<ApiResponse<Appointment[]>>(`${this.apiUrl}/appointments`);
  }

  rescheduleAppointment(id: number, appointmentDate: string): Observable<ApiResponse<Appointment>> {
    return this.http.put<ApiResponse<Appointment>>(`${this.apiUrl}/reschedule/${id}`, {
      appointment_date: appointmentDate
    });
  }
}
