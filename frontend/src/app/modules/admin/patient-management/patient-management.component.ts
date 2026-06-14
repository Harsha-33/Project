import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { AdminApiService } from '../../../services/admin.service';
import { Patient } from '../../../models';

@Component({
  selector: 'app-patient-management',
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './patient-management.component.html',
  styleUrl: './patient-management.component.css'
})
export class PatientManagementComponent implements OnInit {
  patients: Patient[] = [];
  form: FormGroup;
  editingId: number | null = null;
  message = '';
  error = '';
  showForm = false;

  constructor(private adminApi: AdminApiService, private fb: FormBuilder) {
    this.form = this.fb.group({
      name: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      password: ['Password123'],
      dob: [''],
      gender: [''],
      mobile: [''],
      address: [''],
      medical_history: ['']
    });
  }

  ngOnInit(): void {
    this.load();
  }

  load(): void {
    this.adminApi.getPatients().subscribe((res) => {
      if (res.success) this.patients = res.data;
    });
  }

  openAdd(): void {
    this.editingId = null;
    this.form.reset({ password: 'Password123' });
    this.showForm = true;
  }

  openEdit(p: Patient): void {
    this.editingId = p.patient_id;
    this.form.patchValue(p);
    this.showForm = true;
  }

  save(): void {
    if (this.form.invalid) return;
    const data = this.form.value;
    const req = this.editingId
      ? this.adminApi.updatePatient(this.editingId, data)
      : this.adminApi.addPatient(data);

    req.subscribe({
      next: (res) => { this.message = res.message; this.showForm = false; this.load(); },
      error: (err) => (this.error = err.error?.message)
    });
  }

  delete(id: number): void {
    if (!confirm('Delete this patient?')) return;
    this.adminApi.deletePatient(id).subscribe({
      next: (res) => { this.message = res.message; this.load(); },
      error: (err) => (this.error = err.error?.message)
    });
  }
}
