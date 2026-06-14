import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule } from '@angular/forms';
import { DatePipe } from '@angular/common';
import { PatientApiService } from '../../../services/patient.service';
import { Appointment } from '../../../models';

@Component({
  selector: 'app-patient-appointments',
  standalone: true,
  imports: [ReactiveFormsModule, DatePipe],
  templateUrl: './patient-appointments.component.html',
  styleUrl: './patient-appointments.component.css'
})
export class PatientAppointmentsComponent implements OnInit {
  appointments: Appointment[] = [];
  rescheduleForm: FormGroup;
  selectedId: number | null = null;
  message = '';
  error = '';

  constructor(private patientApi: PatientApiService, private fb: FormBuilder) {
    this.rescheduleForm = this.fb.group({
      appointment_date: [''],
      appointment_time: ['']
    });
  }

  ngOnInit(): void {
    this.loadAppointments();
  }

  loadAppointments(): void {
    this.patientApi.getUpcoming().subscribe((res) => {
      if (res.success) this.appointments = res.data;
    });
  }

  startReschedule(id: number): void {
    const appointment = this.appointments.find((item) => item.appointment_id === id);
    if (appointment && !this.canReschedule(appointment)) {
      this.error = 'Appointment cannot be rescheduled within 1 hour after booking.';
      return;
    }
    this.error = '';
    this.selectedId = id;
  }

  canReschedule(appointment: Appointment): boolean {
    if (!appointment.created_at) return true;
    const createdAt = new Date(appointment.created_at).getTime();
    return Date.now() >= createdAt + 60 * 60 * 1000;
  }

  submitReschedule(): void {
    if (!this.selectedId) return;
    const { appointment_date, appointment_time } = this.rescheduleForm.value;
    const dateTime = `${appointment_date}T${appointment_time}:00`;

    this.patientApi.reschedule(this.selectedId, dateTime).subscribe({
      next: (res) => {
        this.message = res.message;
        this.error = '';
        this.selectedId = null;
        this.loadAppointments();
      },
      error: (err) => (this.error = err.error?.message || 'Reschedule failed')
    });
  }
}
