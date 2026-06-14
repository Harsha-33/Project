import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { AdminApiService } from '../../../services/admin.service';
import { Doctor } from '../../../models';

@Component({
  selector: 'app-doctor-management',
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './doctor-management.component.html',
  styleUrl: './doctor-management.component.css'
})
export class DoctorManagementComponent implements OnInit {
  doctors: Doctor[] = [];
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
      speciality: [''],
      experience: [0],
      qualification: [''],
      designation: [''],
      phone: ['']
    });
  }

  ngOnInit(): void {
    this.load();
  }

  load(): void {
    this.adminApi.getDoctors().subscribe((res) => {
      if (res.success) this.doctors = res.data;
    });
  }

  openAdd(): void {
    this.editingId = null;
    this.form.reset({ password: 'Password123', experience: 0 });
    this.showForm = true;
  }

  openEdit(doc: Doctor): void {
    this.editingId = doc.doctor_id;
    this.form.patchValue(doc);
    this.showForm = true;
  }

  save(): void {
    if (this.form.invalid) return;
    const data = this.form.value;

    const req = this.editingId
      ? this.adminApi.updateDoctor(this.editingId, data)
      : this.adminApi.addDoctor(data);

    req.subscribe({
      next: (res) => {
        this.message = res.message;
        this.showForm = false;
        this.load();
      },
      error: (err) => (this.error = err.error?.message)
    });
  }

  delete(id: number): void {
    if (!confirm('Delete this doctor?')) return;
    this.adminApi.deleteDoctor(id).subscribe({
      next: (res) => { this.message = res.message; this.load(); },
      error: (err) => (this.error = err.error?.message)
    });
  }
}
