import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { Character } from '../interfaces/character';
import { StorageService } from './token-storage.service';

const API = 'http://localhost:8000/';
@Injectable({
  providedIn: 'root',
})
export class CharacterService{
  constructor(private http: HttpClient) {};

  private characterSubject$ = new BehaviorSubject<Character>(this.getCharacter())
  character$: Observable<Character> = this.characterSubject$.asObservable();
  updateCharacter(updatedCharacter: Character): void {
    this.characterSubject$.next(updatedCharacter);
  }
  private getCharacter(): any {
    return this.http.get(API + 'characters/user_character/').subscribe((response) => {
      return response});;
  }
}