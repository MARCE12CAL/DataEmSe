import { Routes } from '@angular/router';
import { HomeComponent } from './features/home/home.component';
import { AutodetectComponent } from './features/autodetect/autodetect.component';
import { ProfilesComponent } from './features/profiles/profiles.component';
import { BatchComponent } from './features/batch/batch.component';
import { ScannerComponent } from './features/scanner/scanner.component';
import { UnifierComponent } from './features/unifier/unifier.component';
import { ComparatorComponent } from './features/comparator/comparator.component';
import { ExporterComponent } from './features/exporter/exporter.component';

export const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'autodetect', component: AutodetectComponent },
  { path: 'profiles', component: ProfilesComponent },
  { path: 'batch', component: BatchComponent },
  { path: 'scanner', component: ScannerComponent },
  { path: 'unifier', component: UnifierComponent },
  { path: 'comparator', component: ComparatorComponent },
  { path: 'exporter', component: ExporterComponent },
  { path: '**', redirectTo: '' }
];
