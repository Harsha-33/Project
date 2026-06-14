import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { ApiResponse, Appointment, DashboardStats, Doctor, MedicalTest, Prescription } from '../models';

@Injectable({ providedIn: 'root' })
export class DoctorApiService {
  private apiUrl = `${environment.apiUrl}/doctor`;

  constructor(private http: HttpClient) {}

  getAppointments(): Observable<ApiResponse<Appointment[]>> {
    return this.http.get<ApiResponse<Appointment[]>>(`${this.apiUrl}/appointments`);
  }

  acceptAppointment(id: number): Observable<ApiResponse<Appointment>> {
    return this.http.put<ApiResponse<Appointment>>(`${this.apiUrl}/accept/${id}`, {});
  }

  rejectAppointment(id: number): Observable<ApiResponse<Appointment>> {
    return this.http.put<ApiResponse<Appointment>>(`${this.apiUrl}/reject/${id}`, {});
  }

  addConsultation(data: Record<string, unknown>): Observable<ApiResponse<unknown>> {
    return this.http.post<ApiResponse<unknown>>(`${this.apiUrl}/consultation`, data);
  }

  addPrescription(data: Record<string, unknown>): Observable<ApiResponse<Prescription[]>> {
    return this.http.post<ApiResponse<Prescription[]>>(`${this.apiUrl}/prescription`, data);
  }

  searchMedicines(search: string): Observable<ApiResponse<string[]>> {
    return this.http.get<ApiResponse<string[]>>(`${this.apiUrl}/medicines`, { params: { search } });
  }

  addTest(data: Record<string, unknown>): Observable<ApiResponse<MedicalTest>> {
    return this.http.post<ApiResponse<MedicalTest>>(`${this.apiUrl}/test`, data);
  }

  getDashboard(): Observable<ApiResponse<DashboardStats>> {
    return this.http.get<ApiResponse<DashboardStats>>(`${this.apiUrl}/dashboard`);
  }

  getProfile(): Observable<ApiResponse<Doctor>> {
    return this.http.get<ApiResponse<Doctor>>(`${this.apiUrl}/profile`);
  }
}
