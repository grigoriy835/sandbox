import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';
import {FormsModule} from '@angular/forms'

import {AppComponent} from './components/app.component/app.component';
import {BitchezComponent} from './components/bitchez/bitchez.component';
import {BitchDetailComponent} from './components/bitch-detail/bitch-detail.component';
import { MessagesComponent } from './components/messages/messages.component';
import { AppRoutingModule } from './app-routing.module';

@NgModule({
  declarations: [
    AppComponent,
    BitchezComponent,
    BitchDetailComponent,
    MessagesComponent
  ],
  imports: [
    FormsModule,
    BrowserModule,
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule {
}
