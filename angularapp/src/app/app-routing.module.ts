import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { BitchezComponent } from './components/bitchez/bitchez.component';
import { DashboardComponent } from "./components/dashboard/dashboard.component";
import { BitchDetailComponent} from "./components/bitch-detail/bitch-detail.component";


const routes: Routes = [
  { path: 'bitchez', component: BitchezComponent },
  { path: 'dashboard', component: DashboardComponent },
  { path: '', redirectTo: '/dashboard', pathMatch: 'full' },
  { path: 'detail/:id', component: BitchDetailComponent }
];


@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
