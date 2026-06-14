import { Component, OnInit } from '@angular/core';
import { RouterLink } from '@angular/router';
import { AdminApiService } from '../../../services/admin.service';
import { DashboardStats } from '../../../models';

@Component({
  selector: 'app-admin-dashboard',
  standalone: true,
  imports: [RouterLink],
  templateUrl: './admin-dashboard.component.html',
  styleUrl: './admin-dashboard.component.css'
})
export class AdminDashboardComponent implements OnInit {
  stats: DashboardStats = {};

  constructor(private adminApi: AdminApiService) {}

  ngOnInit(): void {
    this.adminApi.getDashboard().subscribe((res) => {
      if (res.success) this.stats = res.data;
    });
  }
}
