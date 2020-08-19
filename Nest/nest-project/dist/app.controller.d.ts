import { AppService } from './app.service';
import { Response } from 'express';
export declare class AppController {
    private appService;
    constructor(appService: AppService);
    root(res: Response): void;
}
