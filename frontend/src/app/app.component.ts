import { Component } from '@angular/core';
import { StorageService } from './_services/token-storage.service';
import { AuthService } from './_services/auth.service';
import { CharacterService } from './_services/character.service';
import { Character } from './interfaces/character';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
  providers: [CharacterService],
})
export class AppComponent {
  isLoggedIn = false;
  showAdminBoard = false;
  showModeratorBoard = false;
  character?: Character;
  levelPercent?: number;
  username?: string;

  constructor(
    private storageService: StorageService,
    private authService: AuthService,
    private characterService: CharacterService,
    ) {}

  ngOnInit(): void {
    this.isLoggedIn = this.storageService.isLoggedIn();
    if (this.isLoggedIn) {
      const user = this.storageService.getUser();

      this.username = user.username;
      this.characterService.character$.subscribe(
        character => {this.character = character; this.levelPercent = character.currentExp / Math.pow(character.level, 3) * 100}
      )
    }
  }

  logout(): void {
    this.authService.logout().subscribe({
      next: res => {
        console.log(res);
        this.storageService.clean();
      },
      error: err => {
        console.log(err);
      }
    });
    
    window.location.reload();
  }
}