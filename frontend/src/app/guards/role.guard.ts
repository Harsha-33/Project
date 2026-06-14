import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { AuthService } from '../services/auth.service';

export const roleGuard = (roles: string[]): CanActivateFn => {
  return () => {
    const auth = inject(AuthService);
    const router = inject(Router);
    const userRole = auth.getRole();

    if (userRole && roles.includes(userRole)) {
      return true;
    }

    router.navigate(['/auth/login']);
    return false;
  };
};
