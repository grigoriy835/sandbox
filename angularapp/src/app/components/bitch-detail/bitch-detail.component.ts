import { Component, OnInit, Input } from '@angular/core';
import {Bitch} from "../../models/bitch";

@Component({
  selector: 'app-bitch-detail',
  templateUrl: './bitch-detail.component.html',
  styleUrls: ['./bitch-detail.component.css']
})
export class BitchDetailComponent implements OnInit {

  @Input()
  bitch: Bitch;

  constructor() { }

  ngOnInit() {
  }

}
