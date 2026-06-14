import { Component, OnInit } from '@angular/core';
import { DoctorApiService } from '../../../services/doctor.service';
import { Doctor } from '../../../models';

@Component({
  selector: 'app-doctor-profile',
  standalone: true,
  imports: [],
  templateUrl: './doctor-profile.component.html',
  styleUrl: './doctor-profile.component.css'
})
export class DoctorProfileComponent implements OnInit {
  profile: Doctor | null = null;
  error = '';
  loading = true;

  constructor(private doctorApi: DoctorApiService) {}

  ngOnInit(): void {
    this.doctorApi.getProfile().subscribe({
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
