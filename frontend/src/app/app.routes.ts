import { Routes } from '@angular/router';
import { authGuard, guestGuard } from './guards/auth.guard';
import { roleGuard } from './guards/role.guard';
import { MainLayoutComponent } from './layouts/main-layout/main-layout.component';
import { LoginComponent } from './modules/auth/login/login.component';
import { RegisterComponent } from './modules/auth/register/register.component';
import { ForgotPasswordComponent } from './modules/auth/forgot-password/forgot-password.component';
import { PatientDashboardComponent } from './modules/patient/dashboard/patient-dashboard.component';
import { BookAppointmentComponent } from './modules/patient/book-appointment/book-appointment.component';
import { PatientAppointmentsComponent } from './modules/patient/appointments/patient-appointments.component';
import { ConsultationHistoryComponent } from './modules/patient/consultation-history/consultation-history.component';
import { PatientProfileComponent } from './modules/patient/profile/patient-profile.component';
import { DoctorDashboardComponent } from './modules/doctor/dashboard/doctor-dashboard.component';
import { DoctorAppointmentsComponent } from './modules/doctor/appointments/doctor-appointments.component';
import { ConsultationComponent } from './modules/doctor/consultation/consultation.component';
import { DoctorProfileComponent } from './modules/doctor/profile/doctor-profile.component';
import { AdminDashboardComponent } from './modules/admin/dashboard/admin-dashboard.component';
import { DoctorManagementComponent } from './modules/admin/doctor-management/doctor-management.component';
import { PatientManagementComponent } from './modules/admin/patient-management/patient-management.component';
import { AppointmentManagementComponent } from './modules/admin/appointment-management/appointment-management.component';

export const routes: Routes = [
  { path: '', redirectTo: 'auth/login', pathMatch: 'full' },
  {
    path: 'auth',
    canActivate: [guestGuard],
    children: [
      { path: 'login', component: LoginComponent },
      { path: 'register', component: RegisterComponent },
      { path: 'forgot-password', component: ForgotPasswordComponent }
    ]
  },
  {
    path: '',
    component: MainLayoutComponent,
    canActivate: [authGuard],
    children: [
      {
        path: 'patient',
        canActivate: [roleGuard(['PATIENT'])],
        children: [
          { path: 'dashboard', component: PatientDashboardComponent },
          { path: 'book-appointment', component: BookAppointmentComponent },
          { path: 'appointments', component: PatientAppointmentsComponent },
          { path: 'history', component: ConsultationHistoryComponent },
          { path: 'profile', component: PatientProfileComponent }
        ]
      },
      {
        path: 'doctor',
        canActivate: [roleGuard(['DOCTOR'])],
        children: [
          { path: 'dashboard', component: DoctorDashboardComponent },
          { path: 'appointments', component: DoctorAppointmentsComponent },
          { path: 'consultation/:id', component: ConsultationComponent },
          { path: 'profile', component: DoctorProfileComponent }
        ]
      },
      {
        path: 'admin',
        canActivate: [roleGuard(['ADMIN'])],
        children: [
          { path: 'dashboard', component: AdminDashboardComponent },
          { path: 'doctors', component: DoctorManagementComponent },
          { path: 'patients', component: PatientManagementComponent },
          { path: 'appointments', component: AppointmentManagementComponent }
        ]
      }
    ]
  },
  { path: '**', redirectTo: 'auth/login' }
];
