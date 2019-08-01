import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { BitchezComponent } from './components/bitchez/bitchez.component';


const routes: Routes = [
  { path: 'bitchez', component: BitchezComponent }
];


@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
