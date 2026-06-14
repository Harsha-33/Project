import { Component, OnInit } from '@angular/core';
import { DatePipe } from '@angular/common';
import { RouterLink } from '@angular/router';
import { DoctorApiService } from '../../../services/doctor.service';
import { Appointment, DashboardStats } from '../../../models';

@Component({
  selector: 'app-doctor-dashboard',
  standalone: true,
  imports: [RouterLink, DatePipe],
  templateUrl: './doctor-dashboard.component.html',
  styleUrl: './doctor-dashboard.component.css'
})
export class DoctorDashboardComponent implements OnInit {
  stats: DashboardStats = {};
  upcomingAppointments: Appointment[] = [];

  constructor(private doctorApi: DoctorApiService) {}

  ngOnInit(): void {
    this.doctorApi.getDashboard().subscribe((res) => {
      if (res.success) this.stats = res.data;
    });
    this.doctorApi.getAppointments().subscribe((res) => {
      if (res.success) {
        this.upcomingAppointments = res.data
          .filter((item) => ['PENDING', 'CONFIRMED', 'ACCEPTED'].includes(item.status))
          .slice(0, 5);
      }
    });
  }
}
