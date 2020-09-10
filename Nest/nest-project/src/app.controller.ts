import { Controller, Get, Render, Res } from '@nestjs/common';
import { AppService } from './app.service';
import { Response } from 'express';

@Controller()
export class AppController {
  constructor(private appService: AppService) { }
  @Get()
  @Render('main/index')
  async root() { }
}

