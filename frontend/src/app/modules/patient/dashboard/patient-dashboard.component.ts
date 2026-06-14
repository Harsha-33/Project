import { Component, OnInit } from '@angular/core';
import { RouterLink } from '@angular/router';
import { PatientApiService } from '../../../services/patient.service';
import { DashboardStats } from '../../../models';

@Component({
  selector: 'app-patient-dashboard',
  standalone: true,
  imports: [RouterLink],
  templateUrl: './patient-dashboard.component.html',
  styleUrl: './patient-dashboard.component.css'
})
export class PatientDashboardComponent implements OnInit {
  stats: DashboardStats = {};

  constructor(private patientApi: PatientApiService) {}

  ngOnInit(): void {
    this.patientApi.getDashboard().subscribe((res) => {
      if (res.success) this.stats = res.data;
    });
  }
}
