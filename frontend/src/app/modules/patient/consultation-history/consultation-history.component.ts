import { Component, OnInit } from '@angular/core';
import { DatePipe } from '@angular/common';
import { PatientApiService } from '../../../services/patient.service';
import { Consultation } from '../../../models';

@Component({
  selector: 'app-consultation-history',
  standalone: true,
  imports: [DatePipe],
  templateUrl: './consultation-history.component.html',
  styleUrl: './consultation-history.component.css'
})
export class ConsultationHistoryComponent implements OnInit {
  history: Consultation[] = [];

  constructor(private patientApi: PatientApiService) {}

  ngOnInit(): void {
    this.patientApi.getHistory().subscribe((res) => {
      if (res.success) this.history = res.data;
    });
  }
}
