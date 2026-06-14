import { Component, OnInit } from '@angular/core';
import { FormArray, FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';
import { DoctorApiService } from '../../../services/doctor.service';

@Component({
  selector: 'app-consultation',
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './consultation.component.html',
  styleUrl: './consultation.component.css'
})
export class ConsultationComponent implements OnInit {
  form: FormGroup;
  prescriptionForm: FormGroup;
  testForm: FormGroup;
  appointmentId = 0;
  consultationId: number | null = null;
  medicineSuggestions: string[][] = [[]];
  message = '';
  error = '';

  constructor(
    private fb: FormBuilder,
    private route: ActivatedRoute,
    private doctorApi: DoctorApiService
  ) {
    this.form = this.fb.group({
      current_symptoms: ['', Validators.required],
      physical_examination: [''],
      diagnosis: ['', Validators.required],
      treatment_plan: ['']
    });
    this.prescriptionForm = this.fb.group({
      prescriptions: this.fb.array([this.createPrescriptionGroup()])
    });
    this.testForm = this.fb.group({
      test_name: ['', Validators.required]
    });
  }

  ngOnInit(): void {
    this.appointmentId = +this.route.snapshot.paramMap.get('id')!;
  }

  get prescriptions(): FormArray {
    return this.prescriptionForm.get('prescriptions') as FormArray;
  }

  createPrescriptionGroup(): FormGroup {
    return this.fb.group({
      medicine_name: ['', Validators.required],
      dosage: [''],
      timing: ['']
    });
  }

  addPrescriptionRow(): void {
    this.prescriptions.push(this.createPrescriptionGroup());
    this.medicineSuggestions.push([]);
  }

  removePrescriptionRow(index: number): void {
    if (this.prescriptions.length === 1) return;
    this.prescriptions.removeAt(index);
    this.medicineSuggestions.splice(index, 1);
  }

  searchMedicines(index: number): void {
    const value = this.prescriptions.at(index).get('medicine_name')?.value || '';
    this.doctorApi.searchMedicines(value).subscribe((res) => {
      if (res.success) this.medicineSuggestions[index] = res.data;
    });
  }

  saveConsultation(): void {
    if (this.form.invalid) return;
    this.doctorApi.addConsultation({
      appointment_id: this.appointmentId,
      ...this.form.value
    }).subscribe({
      next: (res) => {
        this.message = res.message;
        this.consultationId = (res.data as { consultation_id: number }).consultation_id;
      },
      error: (err) => (this.error = err.error?.message)
    });
  }

  addPrescription(): void {
    if (!this.consultationId || this.prescriptionForm.invalid) return;
    this.doctorApi.addPrescription({
      consultation_id: this.consultationId,
      prescriptions: this.prescriptionForm.value.prescriptions
    }).subscribe({
      next: (res) => {
        this.message = res.message;
        this.error = '';
        this.prescriptionForm.setControl('prescriptions', this.fb.array([this.createPrescriptionGroup()]));
        this.medicineSuggestions = [[]];
      },
      error: (err) => (this.error = err.error?.message)
    });
  }

  addTest(): void {
    if (!this.consultationId || this.testForm.invalid) return;
    this.doctorApi.addTest({
      consultation_id: this.consultationId,
      ...this.testForm.value
    }).subscribe({
      next: (res) => {
        this.message = res.message;
        this.testForm.reset();
      },
      error: (err) => (this.error = err.error?.message)
    });
  }
}
