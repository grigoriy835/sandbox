import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';
import {FormsModule} from '@angular/forms'

import {AppComponent} from './components/app.component/app.component';
import {BitchezComponent} from './components/bitchez/bitchez.component';
import { BitchDetailComponent } from './components/bitch-detail/bitch-detail.component';

@NgModule({
  declarations: [
    AppComponent,
    BitchezComponent,
    BitchDetailComponent
  ],
  imports: [
    FormsModule,
    BrowserModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule {
}
