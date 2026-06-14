import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule } from '@angular/forms';
import { DatePipe } from '@angular/common';
import { AdminApiService } from '../../../services/admin.service';
import { Appointment } from '../../../models';

@Component({
  selector: 'app-appointment-management',
  standalone: true,
  imports: [ReactiveFormsModule, DatePipe],
  templateUrl: './appointment-management.component.html',
  styleUrl: './appointment-management.component.css'
})
export class AppointmentManagementComponent implements OnInit {
  appointments: Appointment[] = [];
  rescheduleForm: FormGroup;
  selectedId: number | null = null;
  message = '';
  error = '';

  constructor(private adminApi: AdminApiService, private fb: FormBuilder) {
    this.rescheduleForm = this.fb.group({
      appointment_date: [''],
      appointment_time: ['']
    });
  }

  ngOnInit(): void {
    this.load();
  }

  load(): void {
    this.adminApi.getAppointments().subscribe((res) => {
      if (res.success) this.appointments = res.data;
    });
  }

  startReschedule(id: number): void {
    this.selectedId = id;
  }

  submitReschedule(): void {
    if (!this.selectedId) return;
    const { appointment_date, appointment_time } = this.rescheduleForm.value;
    const dateTime = `${appointment_date}T${appointment_time}:00`;

    this.adminApi.rescheduleAppointment(this.selectedId, dateTime).subscribe({
      next: (res) => {
        this.message = res.message;
        this.selectedId = null;
        this.load();
      },
      error: (err) => (this.error = err.error?.message)
    });
  }
}
