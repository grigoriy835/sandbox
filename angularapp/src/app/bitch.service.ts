import { Injectable } from '@angular/core';
import {Bitch} from './models/bitch';
import {BITCHEZ} from "./mock-bitchez";
import { Observable, of } from 'rxjs';
import { MessageService } from './message.service'

@Injectable({
  providedIn: 'root'
})
export class BitchService {

  constructor(private messageService: MessageService) { }

  getBitchez(): Observable<Bitch[]> {
    // TODO: send the message _after_ fetching the heroes
    this.messageService.add('Hfetched bitchez');
    return of(BITCHEZ);
  }

  getBitch(id: number): Observable<Bitch> {
    this.messageService.add(`fetched bitch if= ${id}`);
    return of(BITCHEZ.find(bitch => bitch.id == id))
  }

}
