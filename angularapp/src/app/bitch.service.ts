import { Injectable } from '@angular/core';
import {Bitch} from './models/bitch';
import {BITCHEZ} from "./mock-bitchez";
import { Observable, of } from 'rxjs';
import { MessageService } from './message.service'

@Injectable({
  providedIn: 'root'
})
export class BitchService {

  getBitchez(): Observable<Bitch[]> {
    // TODO: send the message _after_ fetching the heroes
    this.messageService.add('Hfetched bitchez');
    return of(BITCHEZ);
  }
  constructor(private messageService: MessageService) { }
}
