import {Component, OnInit} from '@angular/core';
import {Bitch} from '../../models/bitch';
import {BITCHEZ} from "../../mock-bitchez";


@Component({
  selector: 'app-bitchez',
  templateUrl: './bitchez.component.html',
  styleUrls: ['./bitchez.component.css']
})
export class BitchezComponent implements OnInit {

  bitchez: Bitch[] = BITCHEZ;

  constructor() {
  }

  ngOnInit() {
  }

  selectedBitch: Bitch;
  onSelect(bitch: Bitch): void {
    this.selectedBitch = bitch;
  }
}
