from typing import List, Optional
from sqlalchemy import Integer, String, Text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector

class Base(DeclarativeBase):
    pass

class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(primary_key=True)
    source: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    tema_texto: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    pregunta_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    pregunta_fecha_creacion: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    pregunta_texto: Mapped[str] = mapped_column(Text)
    respuesta_fecha_actualizacion: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    respuesta_texto: Mapped[str] = mapped_column(Text)
    embedding: Mapped[Optional[Vector]] = mapped_column(Vector(1024), nullable=True)

    tema_links: Mapped[List["TemaLink"]] = relationship(back_populates="document")
    respuesta_links: Mapped[List["RespuestaLink"]] = relationship(back_populates="document")
    preguntas_relacionadas: Mapped[List["PreguntaRelacionada"]] = relationship(back_populates="document")

class TemaLink(Base):
    __tablename__ = "tema_links"

    id: Mapped[int] = mapped_column(primary_key=True)
    document_id: Mapped[int] = mapped_column(ForeignKey("documents.id"))
    texto: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    href: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    document: Mapped["Document"] = relationship(back_populates="tema_links")

class RespuestaLink(Base):
    __tablename__ = "respuesta_links"

    id: Mapped[int] = mapped_column(primary_key=True)
    document_id: Mapped[int] = mapped_column(ForeignKey("documents.id"))
    texto: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    href: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    document: Mapped["Document"] = relationship(back_populates="respuesta_links")

class PreguntaRelacionada(Base):
    __tablename__ = "preguntas_relacionadas"

    id: Mapped[int] = mapped_column(primary_key=True)
    document_id: Mapped[int] = mapped_column(ForeignKey("documents.id"))
    texto: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    href: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    document: Mapped["Document"] = relationship(back_populates="preguntas_relacionadas")