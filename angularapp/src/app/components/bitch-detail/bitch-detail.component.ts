import { Component, OnInit, Input } from '@angular/core';
import {Bitch} from "../../models/bitch";
import {BitchService} from "../../bitch.service";

import { ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';


@Component({
  selector: 'app-bitch-detail',
  templateUrl: './bitch-detail.component.html',
  styleUrls: ['./bitch-detail.component.css']
})
export class BitchDetailComponent implements OnInit {

  @Input()
  bitch: Bitch;

  constructor(
      private route: ActivatedRoute,
      private bitchService: BitchService,
      private location: Location
  ) { }

  ngOnInit() {
    this.getBitch()
  }

  getBitch(): void {
    const id = +this.route.snapshot.paramMap.get('id');
    this.bitchService.getBitch(id)
        .subscribe(bitch => this.bitch = bitch);
  }

  goBack(): void {
    this.location.back();
  }

}
