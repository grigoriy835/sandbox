import {Component, OnInit} from '@angular/core';
import {Bitch} from '../../models/bitch';
import {BitchService} from "../../bitch.service";


@Component({
  selector: 'app-bitchez',
  templateUrl: './bitchez.component.html',
  styleUrls: ['./bitchez.component.css']
})
export class BitchezComponent implements OnInit {

  bitchez: Bitch[];

  constructor(private bitchService: BitchService) {
  }

  ngOnInit() {
    this.getBitchez();
  }

  getBitchez(): void {
    this.bitchService.getBitchez().subscribe(bitchez => this.bitchez = bitchez);
  }

  selectedBitch: Bitch;
  onSelect(bitch: Bitch): void {
    this.selectedBitch = bitch;
  }
}
