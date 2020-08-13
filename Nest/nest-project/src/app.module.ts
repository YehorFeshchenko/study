import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { TypeOrmModule } from '@nestjs/typeorm';
import Contact from './entities/contact/contact.entity';
import { ContactsModule } from './entities/contact/contacts.module'

@Module({
  imports: [ContactsModule,

    TypeOrmModule.forFeature(
      [Contact],
    ),

    TypeOrmModule.forRoot(),
  ],
  controllers: [AppController],
  providers: [AppService],
})

export class AppModule { }