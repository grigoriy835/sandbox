import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { BitchezComponent } from './bitchez.component';

describe('BitchezComponent', () => {
  let component: BitchezComponent;
  let fixture: ComponentFixture<BitchezComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ BitchezComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(BitchezComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
