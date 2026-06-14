import { Component, OnInit } from '@angular/core';
import { DatePipe } from '@angular/common';
import { RouterLink } from '@angular/router';
import { DoctorApiService } from '../../../services/doctor.service';
import { Appointment } from '../../../models';

@Component({
  selector: 'app-doctor-appointments',
  standalone: true,
  imports: [DatePipe, RouterLink],
  templateUrl: './doctor-appointments.component.html',
  styleUrl: './doctor-appointments.component.css'
})
export class DoctorAppointmentsComponent implements OnInit {
  appointments: Appointment[] = [];
  message = '';
  error = '';

  constructor(private doctorApi: DoctorApiService) {}

  ngOnInit(): void {
    this.load();
  }

  load(): void {
    this.doctorApi.getAppointments().subscribe((res) => {
      if (res.success) this.appointments = res.data;
    });
  }

  accept(id: number): void {
    this.doctorApi.acceptAppointment(id).subscribe({
      next: (res) => { this.message = res.message; this.load(); },
      error: (err) => (this.error = err.error?.message)
    });
  }

  reject(id: number): void {
    this.doctorApi.rejectAppointment(id).subscribe({
      next: (res) => { this.message = res.message; this.load(); },
      error: (err) => (this.error = err.error?.message)
    });
  }

  getRowClass(status: string): string {
    if (status === 'ACCEPTED') return 'table-success';
    if (status === 'CONFIRMED') return 'table-success';
    if (status === 'COMPLETED') return 'table-secondary';
    if (status === 'REJECTED') return 'table-danger';
    return '';
  }
}
