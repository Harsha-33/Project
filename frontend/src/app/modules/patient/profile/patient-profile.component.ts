import { Component, OnInit } from '@angular/core';
import { PatientApiService } from '../../../services/patient.service';
import { Patient } from '../../../models';

@Component({
  selector: 'app-patient-profile',
  standalone: true,
  imports: [],
  templateUrl: './patient-profile.component.html',
  styleUrl: './patient-profile.component.css'
})
export class PatientProfileComponent implements OnInit {
  profile: Patient | null = null;
  error = '';
  loading = true;

  constructor(private patientApi: PatientApiService) {}

  ngOnInit(): void {
    this.patientApi.getProfile().subscribe({
      next: (res) => {
        if (res.success) this.profile = res.data;
        this.loading = false;
      },
      error: (err) => {
        this.error = err.error?.message || 'Profile could not be loaded';
        this.loading = false;
      }
    });
  }
}
