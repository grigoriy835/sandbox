import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { BitchDetailComponent } from './bitch-detail.component';

describe('BitchDetailComponent', () => {
  let component: BitchDetailComponent;
  let fixture: ComponentFixture<BitchDetailComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ BitchDetailComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(BitchDetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
