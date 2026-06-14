import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { ApiResponse, Appointment, Consultation, DashboardStats, Doctor, DoctorAvailability, Patient } from '../models';

@Injectable({ providedIn: 'root' })
export class PatientApiService {
  private apiUrl = `${environment.apiUrl}/patient`;

  constructor(private http: HttpClient) {}

  getDoctors(search = '', speciality = ''): Observable<ApiResponse<Doctor[]>> {
    const params: Record<string, string> = {};
    if (search) params['search'] = search;
    if (speciality) params['speciality'] = speciality;
    return this.http.get<ApiResponse<Doctor[]>>(`${this.apiUrl}/doctors`, { params });
  }

  getDoctorAvailability(doctorId: number, date: string): Observable<ApiResponse<DoctorAvailability>> {
    return this.http.get<ApiResponse<DoctorAvailability>>(
      `${this.apiUrl}/doctors/${doctorId}/availability`,
      { params: { date } }
    );
  }

  bookAppointment(data: Record<string, unknown>): Observable<ApiResponse<Appointment>> {
    return this.http.post<ApiResponse<Appointment>>(`${this.apiUrl}/appointment`, data);
  }

  getUpcoming(): Observable<ApiResponse<Appointment[]>> {
    return this.http.get<ApiResponse<Appointment[]>>(`${this.apiUrl}/upcoming`);
  }

  reschedule(id: number, appointmentDate: string): Observable<ApiResponse<Appointment>> {
    return this.http.put<ApiResponse<Appointment>>(`${this.apiUrl}/reschedule/${id}`, {
      appointment_date: appointmentDate
    });
  }

  getHistory(): Observable<ApiResponse<Consultation[]>> {
    return this.http.get<ApiResponse<Consultation[]>>(`${this.apiUrl}/history`);
  }

  getDashboard(): Observable<ApiResponse<DashboardStats>> {
    return this.http.get<ApiResponse<DashboardStats>>(`${this.apiUrl}/dashboard`);
  }

  getProfile(): Observable<ApiResponse<Patient>> {
    return this.http.get<ApiResponse<Patient>>(`${this.apiUrl}/profile`);
  }
}
